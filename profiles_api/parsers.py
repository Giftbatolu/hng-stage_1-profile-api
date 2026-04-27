import re
import pycountry

# Common aliases / abbreviations (pycountry may miss these)
ALIASES = {
    "usa": "US",
    "uk": "GB",
    "uae": "AE",
    "south korea": "KR",
    "north korea": "KP"
}


def extract_country(query: str):
    query = query.lower()

    for alias, code in ALIASES.items():
        if alias in query:
            return code

    try:
        country = pycountry.countries.search_fuzzy(query)[0]
        return country.alpha_2
    except LookupError:
        pass

    for word in query.split():
        try:
            country = pycountry.countries.search_fuzzy(word)[0]
            return country.alpha_2
        except LookupError:
            continue

    return None


def parse_natural_query(query: str):
    query = query.lower().strip()
    filters = {}

    has_male = "male" in query
    has_female = "female" in query

    if "male and female" in query or (has_male and has_female):
        filters["gender"] = None

    elif has_male:
        filters["gender"] = "male"

    elif has_female:
        filters["gender"] = "female"
        
    if "young" in query:
        filters["min_age"] = 16
        filters["max_age"] = 24

    if "teenager" in query or "teenagers" in query:
        filters["age_group"] = "teenager"

    if "adult" in query:
        filters["age_group"] = "adult"

    if "senior" in query:
        filters["age_group"] = "senior"

    match = re.search(r"above\s+(\d+)", query)
    if match:
        filters["min_age"] = int(match.group(1))

    match = re.search(r"below\s+(\d+)", query)
    if match:
        filters["max_age"] = int(match.group(1))

    country_code = extract_country(query)
    if country_code:
        filters["country_id"] = country_code

    return filters if filters else None