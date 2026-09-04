import re


def parse_natural_query(query):
    """
    Parse a natural-language house search query.

    Example:
    "I want a 3 bedroom house in Delhi under 80 lakh
    with 1500 square feet area."
    """

    if not query or not isinstance(query, str):
        return {
            "location": None,
            "bedrooms": None,
            "bathrooms": None,
            "area": None,
            "budget": None,
            "property_type": None,
            "furnishing": None,
        }

    text = query.lower().strip()

    result = {
        "location": None,
        "bedrooms": None,
        "bathrooms": None,
        "area": None,
        "budget": None,
        "property_type": None,
        "furnishing": None,
    }

    # -----------------------------
    # Bedrooms / BHK
    # -----------------------------
    bedroom_match = re.search(
        r"(\d+)\s*(?:bhk|bedroom|bedrooms|bed)",
        text
    )

    if bedroom_match:
        result["bedrooms"] = int(bedroom_match.group(1))

    # -----------------------------
    # Bathrooms
    # -----------------------------
    bathroom_match = re.search(
        r"(\d+)\s*(?:bathroom|bathrooms|bath)",
        text
    )

    if bathroom_match:
        result["bathrooms"] = int(bathroom_match.group(1))

    # -----------------------------
    # Area
    # -----------------------------
    area_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:sq\.?\s*ft|sqft|square\s*feet|square\s*ft)",
        text
    )

    if area_match:
        result["area"] = float(area_match.group(1))

    # -----------------------------
    # Budget
    # -----------------------------
    budget_match = re.search(
        r"(?:under|below|less\s+than|within|max(?:imum)?|upto|up\s+to)"
        r"\s*(?:₹|rs\.?|inr)?\s*"
        r"(\d+(?:\.\d+)?)\s*"
        r"(crore|crores|cr|lakh|lakhs|lac|lacs|million|m)?",
        text
    )

    if budget_match:
        value = float(budget_match.group(1))
        unit = budget_match.group(2)

        if unit:
            unit = unit.lower()

        if unit in ["crore", "crores", "cr"]:
            value *= 10_000_000

        elif unit in ["lakh", "lakhs", "lac", "lacs"]:
            value *= 100_000

        elif unit in ["million", "m"]:
            value *= 1_000_000

        result["budget"] = value

    # -----------------------------
    # Location
    # -----------------------------
    locations = [
        "delhi",
        "lucknow",
        "noida",
        "gurgaon",
        "gurugram",
        "kanpur",
        "prayagraj",
        "jaipur",
        "mumbai",
        "bangalore",
        "bengaluru",
        "pune",
        "hyderabad",
        "chennai",
        "kolkata",
        "ahmedabad",
        "varanasi",
    ]

    for location in locations:
        if location in text:
            result["location"] = location.title()
            break

    # -----------------------------
    # Property Type
    # -----------------------------
    if "villa" in text:
        result["property_type"] = "Villa"

    elif "apartment" in text or "flat" in text:
        result["property_type"] = "Apartment"

    elif "house" in text or "home" in text:
        result["property_type"] = "House"

    # -----------------------------
    # Furnishing
    # -----------------------------
    if "fully furnished" in text:
        result["furnishing"] = "Furnished"

    elif "semi furnished" in text or "semi-furnished" in text:
        result["furnishing"] = "Semi-Furnished"

    elif "unfurnished" in text or "un furnished" in text:
        result["furnishing"] = "Unfurnished"

    return result


if __name__ == "__main__":
    examples = [
        "I want a 3 bedroom house in Delhi under 80 lakh with 1500 square feet area.",
        "Find a 2 BHK apartment in Lucknow below 50 lakh.",
        "I need a 4 bedroom villa in Mumbai under 2 crore.",
    ]

    for example in examples:
        print("\nQuery:", example)
        print("Result:", parse_natural_query(example))