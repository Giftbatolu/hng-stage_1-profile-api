import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_url(url):
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # raises error for bad HTTP status
    return response.json()

def fetch_external_data(name):
    urls = {
        "gender": f"https://api.genderize.io?name={name}",
        "age": f"https://api.agify.io?name={name}",
        "nation": f"https://api.nationalize.io?name={name}",
    }

    results = {}

    try:
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_key = {
                executor.submit(fetch_url, url): key
                for key, url in urls.items()
            }

            for future in as_completed(future_to_key):
                key = future_to_key[future]
                results[key] = future.result()

    except requests.RequestException:
        return None, "Upstream or server failure"
    except Exception:
        return None, "Unexpected error"

    # Validation
    gender = results.get("gender")
    age = results.get("age")
    nation = results.get("nation")

    if gender.get("gender") is None or gender.get("count", 0) == 0:
        return None, "Genderize returned an invalid response"

    if age.get("age") is None:
        return None, "Agify returned an invalid response"

    if not nation.get("country"):
        return None, "Nationalize returned an invalid response"

    return results, None