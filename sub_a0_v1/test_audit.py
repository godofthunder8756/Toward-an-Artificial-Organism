import numpy as np
import pytest

from sub_a0_v1.audit import reconstruct, trace_hashes


def rows() -> list[dict[str, object]]:
    return [
        {"tick": i + 1, "query": i % 16, "prediction": [0] * 16, "correct": 16,
         "writes_r": 0, "writes_t": 0, "attempts": 256}
        for i in range(1024)
    ]


def test_newline_translation_is_not_content_corruption() -> None:
    lf = b'{"tick":1}\n{"tick":2}\n'
    crlf = lf.replace(b"\n", b"\r\n")
    assert trace_hashes(lf)["lf_normalized_sha256"] == trace_hashes(crlf)["lf_normalized_sha256"]
    assert trace_hashes(lf)["physical_sha256"] != trace_hashes(crlf)["physical_sha256"]
    assert trace_hashes(lf)["lf_normalized_sha256"] != trace_hashes(lf.replace(b"2", b"3"))["lf_normalized_sha256"]


def test_full_planned_horizon_includes_no_allocation() -> None:
    result = reconstruct(rows(), np.zeros((16, 16)))
    assert result["A"] == 0 and result["accuracy"] == 1
    assert result["opportunities_r"] == 126 * 1024
    assert result["opportunities_t"] == 768 * 1024


@pytest.mark.parametrize("key,value", [
    ("tick", 5), ("correct", 0), ("writes_r", 127), ("attempts", 257),
    ("query", 16), ("prediction", [1] * 15),
])
def test_raw_data_corruption_is_rejected(key: str, value: object) -> None:
    trace = rows()
    trace[0][key] = value
    with pytest.raises(RuntimeError):
        reconstruct(trace, np.zeros((16, 16)))


def test_incomplete_coverage_is_not_success() -> None:
    with pytest.raises(RuntimeError, match="coverage"):
        reconstruct(rows()[:-1], np.zeros((16, 16)))
