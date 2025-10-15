import requests

BASE_URL = "http://localhost:9090"

def submission(age: int, gender: str, has_house: str, marital_status: str, income: float):
    url_prediction = f"{BASE_URL}/go_api/predict"
    payload = {
        "age": int(age),
        "gender": gender,
        "has_house": has_house,
        "marital_status": marital_status,
        "income": float(income),
    }
    try:
        resp = requests.post(url_prediction, json=payload, timeout=5)
    except requests.RequestException as e:
        return None, f"request error: {e}"

    if 200 <= resp.status_code < 300:
        try:
            data = resp.json()
        except ValueError:
            return None, f"invalid JSON from server: {resp.text[:200]}"
        return data.get("prediction"), None
    else:
        return None, f"{resp.status_code}: {resp.text[:200]}"