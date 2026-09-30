from pathlib import Path

from verify_class import check


def test_complete_deployed_class_witness_and_rational_upper():
    result = check(Path(__file__).parent / "class_certificate.json")
    assert result["certified"]
    assert result["class_exact"] == "5159249/29296875"
    assert result["upper_numerator"] == 825479840
    assert result["histories"] == 256
    assert result["private_bit_triples"] == 8
