from nlp.query_parser import parse_natural_query


def test_nlp_query():

    result = parse_natural_query(
        "3 bedroom apartment in Delhi under 90 lakh"
    )

    assert result["bedrooms"] == 3
    assert result["location"] == "Delhi"
    assert result["budget"] == 9000000
    assert result["property_type"] == "Apartment"