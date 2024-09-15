"""
Response time - single-threaded
"""

from machine import Pin
import time
import random
import urequests
import ujson as json  # MicroPython uses ujson for JSON handling


import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('ORBI64', 'slowbanana702')

while not wlan.isconnected():
    pass  # Wait until connected

print('Connected to Wi-Fi')



N: int = 10
sample_ms = 10.0
on_ms = 500

def get_formatted_rtc_time():
    rtc = machine.RTC()
    # Get the current datetime as a tuple (year, month, day, weekday, hour, minute, second, microsecond)
    now = rtc.datetime()
    return "{:04}-{:02}-{:02}T{:02}:{:02}:{:02}".format(
        now[0], now[1], now[2], now[4], now[5], now[6])

# Example usage
formatted_time = get_formatted_rtc_time()


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
        min_time = 0
        max_time = 0
        avg_time = 0

    data = {
        "Minimum": min_time,
        "Maximum": max_time,
        "Average": avg_time,
        "Score": len(t_good) / len(t) if len(t) > 0 else 0.0,
        "timestamp": user_uid
    }
    
    print(data["timestamp"])
    print(data["Minimum"])
    print(data["Maximum"])
    print(data["Score"])

    # Send data to API server
    send_data_to_api(data)

    return data

login = 1

def authenticate_user():
    global login
    while True:
        choice = input("Enter 'login' to log in or 'signup' to sign up: ").strip().lower()
        if choice == 'login':
            return login_user()
        elif choice == 'signup':
            login = 0
            return signup_user()
        else:
            print("Invalid choice. Please enter 'login' or 'signup'.")

# Function to sign up the user
def signup_user():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    data = {
        "email": email,
        "password": password
    }
    
    try:
        response = urequests.post("http://172.16.0.9:3000/signup", json=data)
        if response.status_code == 200:
            print("Sign up successful!")
            return response.json()  # Token or user data
        else:
            print(f"Sign up failed: {response.text}")
            return None
    except Exception as e:
        print(f"Error occurred during sign-up: {e}")
        return None

# Function to log in the user
def login_user():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    data = {
        "email": email,
        "password": password
    }
    
    try:
        response = urequests.post("http://172.16.0.9:3000/login", json=data)
        if response.status_code == 200:
            print("Login successful!")
            return response.json()  # Token or user data
        else:
            print(f"Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"Error occurred during login: {e}")
        return None


def retrieve_user_data(uid: str) -> None:
    """Retrieve the user's data from Firebase by UID."""
    url = f"http://172.16.0.9:3000/get_user_data/{uid}"  # Adjust the IP/URL as needed
    
    try:
        response = urequests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("User Data:", data)
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred while retrieving data: {e}")


def send_data_to_api(data: dict) -> None:
    """Sends the game score data to the API server."""
    url = "http://172.16.0.9:3000/upload_score"  # API endpoint for the JS server
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = urequests.get('http://google.com')
        print(response.status_code)
    except Exception as e:
        print(f"Error occurred while making GET request: {e}")

    try:
        print(json.dumps(data))
        headers = {'Content-Type': 'application/json'}
        response = urequests.post(url, headers=headers, data=json.dumps(data))
        print(response.status_code)
        if response.status_code == 200:
            print("Data successfully sent to the API server.")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
            print(response.json())

    except Exception as e:
        print(f"Error occurred while sending data!: {e}")
        raise



if __name__ == "__main__":
    
    user_data = authenticate_user()
    print(user_data)
    if login == 1:
        user_uid = user_data['user']['uid']
    else:
        user_uid = user_data['userRecord']['uid']
    if user_data is None:
        print("Authentication failed. Exiting...")
        sys.exit()
    
    # Prompt the user for their choice
    user_choice = input("Type 'play' to play the game or 'view' to see your data: ").strip().lower()
    
    if user_choice == "view":
        # If they want to view their data, retrieve it
        retrieve_user_data(user_uid)
    elif user_choice == "play":
        # If they want to play, continue with the game
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
