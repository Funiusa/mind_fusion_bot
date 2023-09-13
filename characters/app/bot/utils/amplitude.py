from app.core.config import settings
import requests
import json


def send_to_amplitude(event_type: str):
    headers = {"Content-Type": "application/json", "Accept": "*/*"}
    data = {
        "api_key": "7227d521cc516e686af9441fb386826e",
        "events": [{"device_id": settings.DEVICE_ID, "event_type": event_type}],
    }

    response = requests.post(
        "https://api2.amplitude.com/2/httpapi", headers=headers, data=json.dumps(data)
    )

    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Error:", response.text)
