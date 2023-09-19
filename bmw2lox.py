"""A python script to send state information of your BMW car to a Loxone Miniserver."""
import asyncio
import socket
from bimmer_connected.account import MyBMWAccount # pylint: disable=import-error
from bimmer_connected.api.regions import Regions  # pylint: disable=import-error


# *****************************************************************************
# ENTER YOUR CREDENTIALS HERE:
# BMW login data
USERNAME = 'some@email.com'
PASSWORD = 'YourSuperSecurePassword'
VIN = 'VinOfYourCar'

# Loxone Miniserver IP and UDP target port
MINISERVER_IP = "192.168.1.30"
MINISERVER_PORT = 1234
# *****************************************************************************


# Print a message indicating the start of the BMW request process
print("Starting BMW request")

# Create a BMW account object and authenticate with the provided credentials
account = MyBMWAccount(USERNAME, PASSWORD, Regions.REST_OF_WORLD)

# Retrieve vehicle information
asyncio.run(account.get_vehicles())

# Get the specific vehicle associated with the provided VIN
vehicle = account.get_vehicle(VIN)

# Check if the car is locked
if ".SECURED" in str(vehicle.doors_and_windows.door_lock_state) or \
   ".LOCKED"  in str(vehicle.doors_and_windows.door_lock_state):
    CAR_LOCKED = 1
else:
    CAR_LOCKED = 0

# Check if the car is charging
if ".CHARGING" in str(vehicle.fuel_and_battery.charging_status):
    CAR_CHARGING = 1
else:
    CAR_CHARGING = 0

# Multiply coordinates by 10 (Loxone can only recognize 3 characters after the comma)
latitude = vehicle.vehicle_location.location.latitude * 10.0
longitude = vehicle.vehicle_location.location.longitude * 10.0

# Create a dictionary containing data to be sent to Loxone
data_for_loxone = {"all_lids_closed":       int(vehicle.doors_and_windows.all_lids_closed),
                   "all_windows_closed":    int(vehicle.doors_and_windows.all_windows_closed),
                   "car_locked":            CAR_LOCKED,
                   "charging_level_hv":     vehicle.fuel_and_battery.remaining_battery_percent,
                  #"charging_start_time":   vehicle.fuel_and_battery.charging_start_time,
                  #"charging_end_time":     vehicle.fuel_and_battery.charging_end_time,
                   "is_charger_connected":  int(vehicle.fuel_and_battery.is_charger_connected),
                   "is_charging":           CAR_CHARGING,
                  #"last_update":           vehicle.data["state"]["lastUpdatedAt"],
                   "latitude_x10":          latitude,
                   "longitude_x10":         longitude}

# Print the data to be sent to Loxone
print(data_for_loxone)

# Create a UDP socket for communication with the Loxone Miniserver
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send the data as bytes in UTF-8 encoding to the specified Miniserver IP and port
sock.sendto(bytes(str(data_for_loxone), "utf-8"), (MINISERVER_IP, MINISERVER_PORT))
