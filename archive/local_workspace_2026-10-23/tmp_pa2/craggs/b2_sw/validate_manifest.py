#!/usr/bin/env python3
"""Validation and freezing utilities for ToE experiment manifests.

Supports:
  validate             JSON Schema + semantic/cross-field validation
  freeze               validate, hash manifest/referenced files, write lock file
  verify-frozen        verify manifest and referenced files against lock file
  validate-provenance  validate a completed run provenance record
  validate-decision    validate a final decision record and preserve INVALID_RUN separation

Designed for the Theory of Everything Research Programme Stage A infrastructure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator

SEMVER_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
WILDCARD_VERSION_TOKENS = {"latest", "current", "head", "master", "main", "*", "x", "X"}
ALLOWED_DECISIONS = {"RETAIN", "RESTRICT", "REDUCE", "SUSPEND", "REJECT"}
VALIDITY_STATES = {"VALID_POSITIVE", "VALID_NEGATIVE", "VALID_MIXED", "INVALID_RUN"}


@dataclass
class ValidationIssue:
    code: str
    message: str
    path: str = ""

    def __str__(self) -> str:
        where = f" [{self.path}]" if self.path else ""
        return f"{self.code}{where}: {self.message}"


def load_structured(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    if suffix == ".json":
        return json.loads(text)
    # Try YAML first because JSON is valid YAML.
    return yaml.safe_load(text)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def path_str(parts: Iterable[Any]) -> str:
    return ".".join(str(p) for p in parts)


def schema_validate(manifest: dict[str, Any], schema: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    validator = Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(manifest), key=lambda e: list(e.absolute_path)):
        issues.append(
            ValidationIssue(
                "SCHEMA",
                err.message,
                path_str(err.absolute_path),
            )
        )
    return issues


def resolve_project_path(project_root: Path, rel_path: str) -> Path:
    p = (project_root / rel_path).resolve()
    root = project_root.resolve()
    try:
        p.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Path escapes project root: {rel_path}") from exc
    return p


def load_registry_ids(project_root: Path, rel_path: str) -> tuple[set[str], list[ValidationIssue]]:
    issues: list[ValidationIssue] = []
    try:
        p = resolve_project_path(project_root, rel_path)
    except ValueError as exc:
        return set(), [ValidationIssue("V012", str(exc), rel_path)]
    if not p.exists():
        return set(), [ValidationIssue("V012", "Registry file does not exist", rel_path)]
    try:
        data = load_structured(p)
    except Exception as exc:  # noqa: BLE001
        return set(), [ValidationIssue("V012", f"Cannot parse registry: {exc}", rel_path)]

    if isinstance(data, dict):
        items = data.get("items", data.get("registry", data.get("entries")))
    else:
        items = data
    if not isinstance(items, list):
        return set(), [ValidationIssue("V012", "Registry must be a list or contain an 'items' list", rel_path)]

    ids: set[str] = set()
    for i, item in enumerate(items):
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            issues.append(ValidationIssue("V012", "Registry entry must contain string id", f"{rel_path}[{i}]"))
            continue
        if item["id"] in ids:
            issues.append(ValidationIssue("V015", f"Duplicate registry id {item['id']}", rel_path))
        ids.add(item["id"])
    return ids, issues


def all_manifest_object_ids(m: dict[str, Any]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    def add(path: str, value: Any) -> None:
        if isinstance(value, str):
            out.append((path, value))

    add("experiment.id", m.get("experiment", {}).get("id"))
    add("hypothesis.id", m.get("hypothesis", {}).get("id"))
    add("environment.id", m.get("environment", {}).get("id"))
    add("evaluation.suite_id", m.get("evaluation", {}).get("suite_id"))
    for i, x in enumerate(m.get("architectures", []) or []):
        add(f"architectures[{i}].id", x.get("id"))
    for group in ("primary", "secondary"):
        for i, x in enumerate((m.get("estimands", {}) or {}).get(group, []) or []):
            add(f"estimands.{group}[{i}].id", x.get("id"))
    for key in ("interventions", "rescues", "bypasses", "invalid_run_conditions"):
        for i, x in enumerate(m.get(key, []) or []):
            add(f"{key}[{i}].id", x.get("id"))
    for i, x in enumerate((m.get("decision", {}) or {}).get("rules", []) or []):
        add(f"decision.rules[{i}].id", x.get("id"))
    return out


def experiment_registry_validate(m: dict[str, Any], registry_path: Path | None) -> list[ValidationIssue]:
    if registry_path is None:
        return []
    issues: list[ValidationIssue] = []
    if not registry_path.exists():
        return [ValidationIssue("V001", "Experiment registry file does not exist", str(registry_path))]
    try:
        data = load_structured(registry_path)
    except Exception as exc:  # noqa: BLE001
        return [ValidationIssue("V001", f"Cannot parse experiment registry: {exc}", str(registry_path))]
    entries = data.get("experiments", []) if isinstance(data, dict) else data
    if not isinstance(entries, list):
        return [ValidationIssue("V001", "Experiment registry must contain a list", str(registry_path))]
    eid = m["experiment"]["id"]
    ver = m["experiment"]["version"]
    for entry in entries:
        if isinstance(entry, dict) and entry.get("id") == eid and entry.get("version") == ver:
            issues.append(ValidationIssue("V001", f"Experiment id/version already registered: {eid} {ver}"))
    return issues


def semantic_validate(
    m: dict[str, Any],
    manifest_path: Path,
    project_root: Path,
    experiment_registry: Path | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    # V001: uniqueness against optional external experiment registry.
    issues.extend(experiment_registry_validate(m, experiment_registry))

    # V002, V003, V004, V017, V018: versions explicit and semver.
    version_fields: list[tuple[str, str]] = [
        ("schema_version", m.get("schema_version", "")),
        ("experiment.version", m.get("experiment", {}).get("version", "")),
        ("environment.version", m.get("environment", {}).get("version", "")),
        ("evaluation.suite_version", m.get("evaluation", {}).get("suite_version", "")),
    ]
    for i, arch in enumerate(m.get("architectures", []) or []):
        version_fields.append((f"architectures[{i}].version", arch.get("version", "")))
    for pth, version in version_fields:
        if isinstance(version, str):
            if version.strip() in WILDCARD_VERSION_TOKENS or any(tok in version.lower() for tok in ("latest", "current")):
                issues.append(ValidationIssue("V018", "Wildcard/floating versions are prohibited", pth))
            elif not SEMVER_RE.fullmatch(version):
                issues.append(ValidationIssue("V002", "Version must use semantic versioning", pth))

    mode = m.get("experiment", {}).get("mode")
    seed_proc = (m.get("seeds") or {}).get("procedure")

    # V005 is enforced at execution by verify-frozen; remind here for confirmatory/replication.
    # V006: registered seeds in confirmatory/replication.
    if mode in {"confirmatory", "replication"} and seed_proc == "generated":
        issues.append(ValidationIssue("V006", f"{mode} mode cannot generate seeds at runtime", "seeds.procedure"))

    # V007 primary estimand ensured by schema; V008 explicit decision rules ensured by schema.
    if mode in {"confirmatory", "replication"}:
        if not (m.get("decision", {}).get("rules") or []):
            issues.append(ValidationIssue("V008", "Confirmatory/replication mode requires explicit decision rules", "decision.rules"))
        # Confirmatory provenance requirements should all be true.
        for key, value in (m.get("provenance") or {}).items():
            if value is not True:
                issues.append(ValidationIssue("V025", "Confirmatory/replication provenance requirements must be true", f"provenance.{key}"))

    claim_type = m.get("hypothesis", {}).get("claim_type")
    # V009 necessity requires bypass.
    if claim_type == "necessity" and not (m.get("bypasses") or []):
        issues.append(ValidationIssue("V009", "Necessity claim requires at least one preregistered bypass", "bypasses"))
    # V010 causal contribution requires intervention.
    if claim_type == "causal_contribution" and not (m.get("interventions") or []):
        issues.append(ValidationIssue("V010", "Causal-contribution claim requires at least one intervention", "interventions"))

    # V011 rescue target must reference intervention listed in manifest.
    intervention_ids = {x.get("id") for x in m.get("interventions", []) or [] if isinstance(x, dict)}
    for i, rescue in enumerate(m.get("rescues", []) or []):
        target = rescue.get("target_intervention_id") if isinstance(rescue, dict) else None
        if target not in intervention_ids:
            issues.append(ValidationIssue("V011", f"Rescue target {target!r} is not a registered manifest intervention", f"rescues[{i}].target_intervention_id"))

    # V012/V013 external registry resolution.
    for key, code in (("interventions", "V012"), ("rescues", "V012"), ("bypasses", "V013")):
        cache: dict[str, set[str]] = {}
        for i, item in enumerate(m.get(key, []) or []):
            if not isinstance(item, dict):
                continue
            reg = item.get("registry")
            obj_id = item.get("id")
            if not reg:
                continue
            if reg not in cache:
                ids, reg_issues = load_registry_ids(project_root, reg)
                cache[reg] = ids
                for ri in reg_issues:
                    ri.code = code
                issues.extend(reg_issues)
            if obj_id not in cache[reg]:
                issues.append(ValidationIssue(code, f"ID {obj_id!r} not found in registry {reg}", f"{key}[{i}]"))

    # V014 duplicate seeds.
    if seed_proc == "explicit":
        seeds = (m.get("seeds") or {}).get("values", []) or []
        if len(seeds) != len(set(seeds)):
            issues.append(ValidationIssue("V014", "Duplicate seeds are prohibited", "seeds.values"))

    # V015 duplicate object IDs within manifest namespaces / globally.
    seen: dict[str, str] = {}
    for pth, obj_id in all_manifest_object_ids(m):
        if obj_id in seen:
            issues.append(ValidationIssue("V015", f"Duplicate object id {obj_id!r}; first used at {seen[obj_id]}", pth))
        else:
            seen[obj_id] = pth

    # V016 training false => zero budget; training true should have positive budget.
    training = m.get("training") or {}
    budget = (training.get("budget") or {}).get("value")
    if training.get("required") is False and budget != 0:
        issues.append(ValidationIssue("V016", "training.required=false requires budget.value=0", "training.budget.value"))
    if training.get("required") is True and isinstance(budget, (int, float)) and budget <= 0:
        issues.append(ValidationIssue("V016", "training.required=true requires budget.value>0", "training.budget.value"))

    # V017 held-out suites fixed in confirmatory mode.
    if mode == "confirmatory" and m.get("evaluation", {}).get("held_out") is not True:
        issues.append(ValidationIssue("V017", "Confirmatory evaluation must be marked held_out=true", "evaluation.held_out"))

    # V021: invalid-run conditions must remain distinct from scientific outcomes.
    allowed = set((m.get("decision") or {}).get("permitted_outcomes", []) or [])
    if "INVALID_RUN" in allowed:
        issues.append(ValidationIssue("V021", "INVALID_RUN must not be a scientific decision outcome", "decision.permitted_outcomes"))
    for i, cond in enumerate(m.get("invalid_run_conditions", []) or []):
        if isinstance(cond, dict) and not str(cond.get("id", "")).startswith("INVALID_"):
            issues.append(ValidationIssue("V021", "Invalid-run condition ids must start with INVALID_", f"invalid_run_conditions[{i}].id"))

    # V022 is enforced by provenance validation below.

    # V023 decision rules refer to existing hypothesis.
    hypothesis_id = m.get("hypothesis", {}).get("id")
    for i, rule in enumerate((m.get("decision") or {}).get("rules", []) or []):
        if rule.get("hypothesis_id") != hypothesis_id:
            issues.append(ValidationIssue("V023", f"Decision rule references unknown hypothesis {rule.get('hypothesis_id')!r}", f"decision.rules[{i}].hypothesis_id"))

    # V024 is enforced structurally; guard against whitespace-only definitions.
    for group in ("primary", "secondary"):
        for i, est in enumerate((m.get("estimands") or {}).get(group, []) or []):
            if not str(est.get("definition", "")).strip():
                issues.append(ValidationIssue("V024", "Estimand definition must be explicit", f"estimands.{group}[{i}].definition"))


    # A5 analysis-contract validation for schema >= 1.1.0.
    schema_version = str(m.get("schema_version", "0.0.0"))
    try:
        major, minor, *_ = [int(x) for x in schema_version.split(".")[:2]]
    except Exception:
        major, minor = 0, 0
    if (major, minor) >= (1, 1):
        analysis = m.get("analysis")
        if not isinstance(analysis, dict):
            issues.append(ValidationIssue("A501", "Schema >=1.1.0 requires an analysis specification", "analysis"))
        else:
            primary_ids = {x.get("id") for x in (m.get("estimands") or {}).get("primary", []) if isinstance(x, dict)}
            if analysis.get("primary_estimand_id") not in primary_ids:
                issues.append(ValidationIssue("A502", "analysis.primary_estimand_id must reference a registered primary estimand", "analysis.primary_estimand_id"))
            if mode in {"confirmatory", "replication"} and int(analysis.get("minimum_confirmatory_runs", 0)) < 2 and m.get("hypothesis", {}).get("claim_type") == "infrastructure":
                issues.append(ValidationIssue("A503", "Deterministic infrastructure reproducibility requires at least two independent confirmatory runs", "analysis.minimum_confirmatory_runs"))
            if analysis.get("pipeline_version") and not SEMVER_RE.fullmatch(str(analysis.get("pipeline_version"))):
                issues.append(ValidationIssue("A504", "analysis.pipeline_version must use semantic versioning", "analysis.pipeline_version"))
            artifacts = analysis.get("artifacts") or {}
            outputs = m.get("outputs") or {}
            mapping = {
                "processed_csv": "require_processed_data",
                "summary_table": "require_table",
                "figure": "require_figure",
                "decision_record": "require_decision_record",
            }
            for akey, okey in mapping.items():
                if outputs.get(okey) is True and artifacts.get(akey) is not True:
                    issues.append(ValidationIssue("A505", f"outputs.{okey}=true requires analysis.artifacts.{akey}=true", f"analysis.artifacts.{akey}"))

    # Referenced project files should exist. This also makes freezing meaningful.
    refs: list[tuple[str, str]] = []
    if m.get("environment", {}).get("config"):
        refs.append(("environment.config", m["environment"]["config"]))
    for i, arch in enumerate(m.get("architectures", []) or []):
        if arch.get("config"):
            refs.append((f"architectures[{i}].config", arch["config"]))
    if seed_proc == "registry" and m.get("seeds", {}).get("file"):
        refs.append(("seeds.file", m["seeds"]["file"]))
    for key in ("interventions", "rescues", "bypasses"):
        for i, item in enumerate(m.get(key, []) or []):
            if isinstance(item, dict) and item.get("registry"):
                refs.append((f"{key}[{i}].registry", item["registry"]))
    for pth, rel in refs:
        try:
            rp = resolve_project_path(project_root, rel)
            if not rp.exists():
                issues.append(ValidationIssue("FILE", "Referenced file does not exist", pth))
        except ValueError as exc:
            issues.append(ValidationIssue("FILE", str(exc), pth))

    return issues


def collect_referenced_files(m: dict[str, Any], project_root: Path) -> dict[str, str]:
    refs: set[str] = set()
    refs.add(m["environment"]["config"])
    refs.update(a["config"] for a in m.get("architectures", []))
    if m.get("seeds", {}).get("procedure") == "registry":
        refs.add(m["seeds"]["file"])
    for key in ("interventions", "rescues", "bypasses"):
        refs.update(x["registry"] for x in m.get(key, []) if isinstance(x, dict) and x.get("registry"))

    out: dict[str, str] = {}
    for rel in sorted(refs):
        p = resolve_project_path(project_root, rel)
        if not p.exists():
            raise FileNotFoundError(f"Referenced file does not exist: {rel}")
        out[rel] = sha256_file(p)
    return out


def git_commit(project_root: Path) -> str | None:
    try:
        res = subprocess.run(
            ["git", "-C", str(project_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return res.stdout.strip()
    except Exception:  # noqa: BLE001
        return None


def freeze_manifest(
    manifest_path: Path,
    lock_path: Path,
    schema_path: Path,
    project_root: Path,
    experiment_registry: Path | None,
    source_commit: str | None,
) -> list[ValidationIssue]:
    m = load_structured(manifest_path)
    schema = load_structured(schema_path)
    issues = schema_validate(m, schema)
    if not issues:
        issues.extend(semantic_validate(m, manifest_path, project_root, experiment_registry))
    if issues:
        return issues
    if m["experiment"]["mode"] not in {"confirmatory", "replication"}:
        issues.append(ValidationIssue("V005", "Only confirmatory or replication manifests may be frozen for decisive execution", "experiment.mode"))
        return issues

    commit = source_commit or git_commit(project_root)
    if m.get("provenance", {}).get("require_source_commit") and not commit:
        return [ValidationIssue("V025", "Source commit is required; provide --source-commit or run inside a Git repository")]

    lock = {
        "lock_schema_version": "1.0.0",
        "experiment_id": m["experiment"]["id"],
        "experiment_version": m["experiment"]["version"],
        "manifest_path": os.path.relpath(manifest_path.resolve(), project_root.resolve()),
        "manifest_sha256": sha256_file(manifest_path),
        "referenced_file_sha256": collect_referenced_files(m, project_root),
        "frozen_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_commit": commit,
    }
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
    return []


def verify_frozen(manifest_path: Path, lock_path: Path, project_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not lock_path.exists():
        return [ValidationIssue("V005", "Frozen confirmatory/replication execution requires a lock file", str(lock_path))]
    lock = load_structured(lock_path)
    if sha256_file(manifest_path) != lock.get("manifest_sha256"):
        issues.append(ValidationIssue("V019", "Manifest hash mismatch: frozen manifest has changed"))
    for rel, expected in (lock.get("referenced_file_sha256") or {}).items():
        try:
            p = resolve_project_path(project_root, rel)
        except ValueError as exc:
            issues.append(ValidationIssue("V020", str(exc), rel))
            continue
        if not p.exists():
            issues.append(ValidationIssue("V020", "Frozen referenced file is missing", rel))
        elif sha256_file(p) != expected:
            issues.append(ValidationIssue("V020", "Frozen referenced configuration/registry changed", rel))
    return issues


def validate_provenance_record(
    m: dict[str, Any], provenance: dict[str, Any], lock: dict[str, Any] | None = None
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    required = {
        "experiment_id",
        "experiment_version",
        "execution_mode",
        "manifest_sha256",
        "software_version",
        "source_commit",
        "environment_id",
        "environment_version",
        "environment_sha256",
        "architecture_hashes",
        "seed",
        "timestamp_utc",
        "runtime_seconds",
    }
    missing = sorted(required - set(provenance))
    for key in missing:
        issues.append(ValidationIssue("V025", "Required provenance field is missing", key))
    if missing:
        return issues

    if provenance["experiment_id"] != m["experiment"]["id"]:
        issues.append(ValidationIssue("V025", "Provenance experiment_id does not match manifest", "experiment_id"))
    if provenance["experiment_version"] != m["experiment"]["version"]:
        issues.append(ValidationIssue("V025", "Provenance experiment_version does not match manifest", "experiment_version"))
    if provenance["execution_mode"] != m["experiment"]["mode"]:
        issues.append(ValidationIssue("V022", "Execution mode does not match manifest; development outputs cannot be relabelled", "execution_mode"))
    if lock and provenance["manifest_sha256"] != lock.get("manifest_sha256"):
        issues.append(ValidationIssue("V019", "Provenance manifest hash does not match frozen lock", "manifest_sha256"))
    if provenance["environment_id"] != m["environment"]["id"]:
        issues.append(ValidationIssue("V025", "Environment id does not match manifest", "environment_id"))
    if provenance["environment_version"] != m["environment"]["version"]:
        issues.append(ValidationIssue("V025", "Environment version does not match manifest", "environment_version"))
    valid_arch_ids = {a["id"] for a in m.get("architectures", [])}
    hashes = provenance.get("architecture_hashes")
    if not isinstance(hashes, dict) or set(hashes) != valid_arch_ids:
        issues.append(ValidationIssue("V025", "architecture_hashes must contain exactly the manifest architecture IDs", "architecture_hashes"))
    if not isinstance(provenance.get("runtime_seconds"), (int, float)) or provenance["runtime_seconds"] < 0:
        issues.append(ValidationIssue("V025", "runtime_seconds must be non-negative", "runtime_seconds"))
    if not isinstance(provenance.get("seed"), int) or provenance["seed"] < 0:
        issues.append(ValidationIssue("V025", "seed must be a non-negative integer", "seed"))
    if m.get("seeds", {}).get("procedure") == "explicit" and provenance.get("seed") not in set(m["seeds"]["values"]):
        issues.append(ValidationIssue("V006", "Provenance seed is not in registered explicit seed set", "seed"))
    return issues


def validate_decision_record(m: dict[str, Any], record: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    required_common = {"experiment_id", "hypothesis_id", "manifest_version", "validity"}
    for key in sorted(required_common - set(record)):
        issues.append(ValidationIssue("DECISION", "Required decision field is missing", key))
    if issues:
        return issues

    if record["experiment_id"] != m["experiment"]["id"]:
        issues.append(ValidationIssue("DECISION", "experiment_id does not match manifest", "experiment_id"))
    if record["hypothesis_id"] != m["hypothesis"]["id"]:
        issues.append(ValidationIssue("V023", "hypothesis_id does not match manifest", "hypothesis_id"))
    if record["manifest_version"] != m["experiment"]["version"]:
        issues.append(ValidationIssue("DECISION", "manifest_version does not match experiment.version", "manifest_version"))
    validity = record.get("validity")
    if validity not in VALIDITY_STATES:
        issues.append(ValidationIssue("DECISION", f"Unknown validity state {validity!r}", "validity"))
        return issues

    decision = record.get("decision")
    if validity == "INVALID_RUN":
        if decision is not None:
            issues.append(ValidationIssue("V021", "INVALID_RUN must not carry a scientific Retain/Restrict/Reduce/Suspend/Reject decision", "decision"))
        if not str(record.get("invalid_reason", "")).strip():
            issues.append(ValidationIssue("V021", "INVALID_RUN requires invalid_reason", "invalid_reason"))
    else:
        if decision not in ALLOWED_DECISIONS:
            issues.append(ValidationIssue("V021", "Valid scientific run requires a permitted scientific decision", "decision"))
        if "invalid_reason" in record and record.get("invalid_reason"):
            issues.append(ValidationIssue("V021", "Valid scientific run must not be assigned an invalid_reason", "invalid_reason"))
    return issues


def print_issues(issues: list[ValidationIssue]) -> int:
    if not issues:
        print("PASS")
        return 0
    print(f"FAIL ({len(issues)} issue{'s' if len(issues) != 1 else ''})")
    for issue in issues:
        print(f" - {issue}")
    return 1


def parse_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--experiment-registry", type=Path)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)

    p_val = sub.add_parser("validate", help="Validate manifest schema and cross-field rules")
    parse_common(p_val)

    p_freeze = sub.add_parser("freeze", help="Validate and freeze a confirmatory/replication manifest")
    parse_common(p_freeze)
    p_freeze.add_argument("--lock", type=Path, required=True)
    p_freeze.add_argument("--source-commit")

    p_verify = sub.add_parser("verify-frozen", help="Verify frozen manifest and referenced file hashes")
    p_verify.add_argument("manifest", type=Path)
    p_verify.add_argument("--lock", type=Path, required=True)
    p_verify.add_argument("--project-root", type=Path, required=True)

    p_prov = sub.add_parser("validate-provenance", help="Validate completed-run provenance")
    p_prov.add_argument("manifest", type=Path)
    p_prov.add_argument("provenance", type=Path)
    p_prov.add_argument("--lock", type=Path)

    p_dec = sub.add_parser("validate-decision", help="Validate final decision record")
    p_dec.add_argument("manifest", type=Path)
    p_dec.add_argument("decision", type=Path)

    args = ap.parse_args()

    if args.command == "verify-frozen":
        return print_issues(verify_frozen(args.manifest, args.lock, args.project_root))

    if args.command == "validate-provenance":
        m = load_structured(args.manifest)
        p = load_structured(args.provenance)
        lock = load_structured(args.lock) if args.lock else None
        return print_issues(validate_provenance_record(m, p, lock))

    if args.command == "validate-decision":
        m = load_structured(args.manifest)
        d = load_structured(args.decision)
        return print_issues(validate_decision_record(m, d))

    manifest = load_structured(args.manifest)
    schema = load_structured(args.schema)
    issues = schema_validate(manifest, schema)
    if not issues:
        issues.extend(semantic_validate(manifest, args.manifest, args.project_root, args.experiment_registry))

    if args.command == "validate":
        return print_issues(issues)

    if args.command == "freeze":
        if issues:
            return print_issues(issues)
        issues = freeze_manifest(
            args.manifest,
            args.lock,
            args.schema,
            args.project_root,
            args.experiment_registry,
            args.source_commit,
        )
        if not issues:
            print(f"Frozen lock written: {args.lock}")
        return print_issues(issues)

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
