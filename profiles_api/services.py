import requests

def fetch_external_data(name):
    try:
        gender = requests.get(f"https://api.genderize.io?name={name}", timeout=5).json()
        age = requests.get(f"https://api.agify.io?name={name}", timeout=5).json()
        nation = requests.get(f"https://api.nationalize.io?name={name}", timeout=5).json()

    except requests.RequestException:
        return None, "Upstream or server failure"
    
    if gender.get("gender") is None or gender.get("count", 0) == 0:
        return None, "Genderize returned an invalid response"

    if age.get("age") is None:
        return None, "Agify returned an invalid response"

    if not nation.get("country"):
        return None, "Nationalize returned an invalid response"

    return {
        "gender": gender,
        "age": age,
        "nation": nation
    }, None