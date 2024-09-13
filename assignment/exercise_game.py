"""
Response time - single-threaded
"""

from machine import Pin
import time
import random
import json
import requests




N: int = 10
sample_ms = 10.0
on_ms = 500


def random_time_interval(tmin: float, tmax: float) -> float:
    """return a random time interval between max and min"""
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
    # %% let user know game started / is over

    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)


def write_json(json_filename: str, data: dict) -> None:
    """Writes data to a JSON file.

    Parameters
    ----------

    json_filename: str
        The name of the file to write to. This will overwrite any existing file.

    data: dict
        Dictionary data to write to the file.
    """

    with open(json_filename, "w") as f:
        json.dump(data, f)


def scorer(t: list[int | None]) -> dict:
    # %% collate results
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]

    print(t_good)

    if len(t_good) > 0:
        min_time = min(t_good)
        max_time = max(t_good)
        avg_time = sum(t_good) / len(t_good)
    else:
        min_time = None
        max_time = None
        avg_time = None

    data = {
        "Minimum": min_time,
        "Maximum": max_time,
        "Average": avg_time,
        "Score": len(t_good) / len(t) if len(t) > 0 else 0.0,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

    # Send data to API server
    print(data.timestamp)
    send_data_to_api(data)

    return data


def send_data_to_api(data: dict) -> None:
    """Sends the game score data to the API server."""
    url = "http://127.0.0.1:3000/upload_score"  # API endpoint for the JS server
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            print("Data successfully sent to the API server.")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
            print(response.json())

    except Exception as e:
        print(f"Error occurred while sending data: {e}")



if __name__ == "__main__":
    # using "if __name__" allows us to reuse functions in other script files

    led = Pin("LED", Pin.OUT)
    button = Pin(16, Pin.IN, Pin.PULL_UP)

    t: list[int | None] = []

    blinker(3, led)

    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()

        tic = time.ticks_ms()
        t0 = None
        while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
            if button.value() == 0:
                t0 = time.ticks_diff(time.ticks_ms(), tic)
                led.low()
                break
        t.append(t0)

        led.low()

    blinker(5, led)

    scorer(t)
