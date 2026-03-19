from app.utils.normalizer import normalize_company_name


def test_normalize_company_name() -> None:
    assert normalize_company_name("株式会社ABC") == "ABC"
    assert normalize_company_name("ABC株式会社") == "ABC"
    assert normalize_company_name("（株）ABC") == "ABC"
    assert normalize_company_name("ＡＢＣ") == "ABC"
    assert normalize_company_name("abc") == "ABC"
