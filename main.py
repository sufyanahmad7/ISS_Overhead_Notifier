import requests
import datetime as dt
import time
import smtplib

# Removed credentials for privacy.
SG_LAT = round(1.311500, 2)
SG_LNG = round(103.821770, 2)
MY_EMAIL = ""
PASSWORD = ""
COUNT = 0

# Get current time.
now = dt.datetime.now()
now_time = now.time()
now_hour = now.hour
now_minute = now.minute

#  Get sunrise and sunset timings.
response = requests.get(url="https://api.sunrise-sunset.org/json?lat=36.7201600&lng=-4.4203400&formatted=0")
response.raise_for_status()
data = response.json()
sunrise = data["results"]["sunrise"].split("T")
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
print(f"Sunrise (hour): {sunrise}")
print(f"Sunset (hour): {sunset}")
print(f"Time Now: {now_hour}:{now_minute}")

# Checks if it is night time.
def is_night():
    if now_hour >= sunset or now_hour <= sunrise:
        return True

# Checks if ISS is overhead.
def is_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    EXACT_ISS_LAT = round(float(response.json()["iss_position"]["latitude"]), 2)
    EXACT_ISS_LNG = round(float(response.json()["iss_position"]["longitude"]), 2)
    MIN_ISS_LAT = round(EXACT_ISS_LAT - 5, 2)
    MAX_ISS_LAT = round(EXACT_ISS_LAT + 5, 2)
    MIN_ISS_LNG = round(EXACT_ISS_LNG - 5, 2)
    MAX_ISS_LNG = round(EXACT_ISS_LNG + 5, 2)
    if MIN_ISS_LAT <= SG_LAT <= MAX_ISS_LAT and MIN_ISS_LNG <= SG_LNG <= MAX_ISS_LNG:
        return True


# Checks if both functions are true.
def full_run():
    global COUNT
    if is_night() and is_overhead():
        print("LOOK OUTSIDE!")
        # Send email with the content below to the person's email address.
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            # Removed credentials for privacy.
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs="",
                                msg=f"Subject:ISS is nearby!!!\n\nGo outside and have a look!".encode("utf-8"))
    else:
        time.sleep(60)
        COUNT += 1
        print(f"{COUNT} runs already.")
        full_run()

full_run()
