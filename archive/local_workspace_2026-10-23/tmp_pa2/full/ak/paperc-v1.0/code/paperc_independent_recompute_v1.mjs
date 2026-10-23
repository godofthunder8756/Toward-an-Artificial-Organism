import fs from "node:fs/promises";
import crypto from "node:crypto";
import path from "node:path";

const DOSE0 = 0;
const DOSE192 = 192;

function median(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const n = sorted.length;
  if (n === 0) throw new Error("median of empty array");
  return n % 2
    ? sorted[(n - 1) / 2]
    : (sorted[n / 2 - 1] + sorted[n / 2]) / 2;
}

function combinations(source, choose) {
  const out = [];
  function visit(start, selected) {
    if (selected.length === choose) {
      out.push([...selected]);
      return;
    }
    for (let i = start; i < source.length; i += 1) {
      selected.push(source[i]);
      visit(i + 1, selected);
      selected.pop();
    }
  }
  visit(0, []);
  return out;
}

function splitHalfP95(perSlug, slugs) {
  // Non-ordered 8/8 partitions: fix the first slug to the left side.
  const anchored = combinations(slugs.slice(1), 7).map((rest) => [slugs[0], ...rest]);
  if (anchored.length !== 6435) throw new Error(`unexpected split count: ${anchored.length}`);
  const diffs = anchored.map((leftSlugs) => {
    const leftSet = new Set(leftSlugs);
    const left = slugs.filter((slug) => leftSet.has(slug)).map((slug) => perSlug[slug]);
    const right = slugs.filter((slug) => !leftSet.has(slug)).map((slug) => perSlug[slug]);
    return Math.abs(median(left) - median(right));
  }).sort((a, b) => a - b);
  return { n_splits: diffs.length, p95_index_1origin: 6114, p95: diffs[6113] };
}

function sha256(bytes) {
  return crypto.createHash("sha256").update(bytes).digest("hex");
}

export async function recompute(directory = path.dirname(new URL(import.meta.url).pathname)) {
  const rawPath = path.join(directory, "INSTRUMENT0_STAGE5_RAW_V1.jsonl");
  const rawBytes = await fs.readFile(rawPath);
  const rows = rawBytes.toString("utf8").trim().split(/\r?\n/).map(JSON.parse);
  if (rows.length !== 261) throw new Error(`expected 261 rows, found ${rows.length}`);

  const slugs = [...new Set(rows.map((row) => row.slug))].sort();
  const doses = [...new Set(rows.map((row) => row.dose))].sort((a, b) => a - b);
  if (slugs.length !== 16) throw new Error(`expected 16 slugs, found ${slugs.length}`);

  const select = (dose, slug) => rows.filter((row) => row.dose === dose && row.slug === slug);
  const perSlug = {
    E1: Object.fromEntries(slugs.map((slug) => [slug,
      median(select(DOSE192, slug).map((row) => row.TRUE.loss_sum / row.TRUE.n_tokens))
      - median(select(DOSE0, slug).map((row) => row.TRUE.loss_sum / row.TRUE.n_tokens))])),
    E2: Object.fromEntries(slugs.map((slug) => [slug,
      median(select(DOSE0, slug).map((row) => row.SWAP.mean_nll - row.TRUE.mean_nll))])),
    E3: Object.fromEntries(slugs.map((slug) => [slug,
      median(select(DOSE192, slug).map((row) => row.TRUE.stop_mass))
      - median(select(DOSE0, slug).map((row) => row.TRUE.stop_mass))])),
  };

  const d0E3 = median(slugs.map((slug) => median(select(DOSE0, slug).map((row) => row.TRUE.stop_mass))));
  const d192E3 = median(slugs.map((slug) => median(select(DOSE192, slug).map((row) => row.TRUE.stop_mass))));
  const bothOrdersChooseA = rows.filter((row) =>
    row.E4_order1.logp_A > row.E4_order1.logp_B
    && row.E4_order2.logp_A > row.E4_order2.logp_B).length;

  const endpoints = {};
  for (const endpoint of ["E1", "E2", "E3"]) {
    const sep = median(Object.values(perSlug[endpoint]));
    const split = splitHalfP95(perSlug[endpoint], slugs);
    endpoints[endpoint] = {
      sep_max: sep,
      split_half_p95: split.p95,
      n_splits: split.n_splits,
      DR: Math.abs(sep) / split.p95,
      MDE: 2 * split.p95,
    };
  }
  endpoints.E3.d0_slug_median = d0E3;
  endpoints.E3.d192_slug_median = d192E3;
  endpoints.E4 = {
    both_orders_choose_A: bothOrdersChooseA,
    denominator: rows.length,
    item_score_when_both_orders_choose_A: 0.5,
    sep_max: 0,
    null_scale: 0,
    status: "UNDEFINED_ENDPOINT",
  };

  return {
    schema: "mythos.paperc_independent_recompute.v1",
    source: { file: path.basename(rawPath), sha256: sha256(rawBytes) },
    n_rows: rows.length,
    n_slugs: slugs.length,
    doses,
    endpoints,
  };
}
