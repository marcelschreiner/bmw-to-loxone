import asyncio
import socket
from bimmer_connected.account import MyBMWAccount
from bimmer_connected.api.regions import Regions


# *********** Config of BMW to Loxone Bridge ***********
# BMW login data
username = 'some@email.com'
password = 'yoursupersecurepassword'
vin = 'VINOFYOURCAR'
# Loxone Miniserver IP and UDP target port
miniserver_ip = "192.168.1.30"
miniserver_port = 1234
# *********** Config of BMW to Loxone Bridge ***********


print("Starting BMW request")
account = MyBMWAccount(username, password, Regions.REST_OF_WORLD)
asyncio.run(account.get_vehicles())
vehicle = account.get_vehicle(vin)

if ".SECURED" in str(vehicle.doors_and_windows.door_lock_state) or \
   ".LOCKED"  in str(vehicle.doors_and_windows.door_lock_state):
    car_locked = 1
else:
    car_locked = 0

if ".CHARGING" in str(vehicle.fuel_and_battery.charging_status):
    car_charging = 1
else:
    car_charging = 0

# Multiply coordinates by 10 (Loxone can only recognize 3 characters after the comma)
latitude = vehicle.vehicle_location.location.latitude * 10.0
longitude = vehicle.vehicle_location.location.longitude * 10.0

data_for_loxone = {"all_lids_closed":       int(vehicle.doors_and_windows.all_lids_closed),
                   "all_windows_closed":    int(vehicle.doors_and_windows.all_windows_closed),
                   "car_locked":            car_locked,
                   "charging_level_hv":     vehicle.fuel_and_battery.remaining_battery_percent,
                  #"charging_start_time":   vehicle.fuel_and_battery.charging_start_time,
                  #"charging_end_time":     vehicle.fuel_and_battery.charging_end_time,
                   "is_charger_connected":  int(vehicle.fuel_and_battery.is_charger_connected),
                   "is_charging":           car_charging,
                  #"last_update":           vehicle.data["state"]["lastUpdatedAt"],
                   "latitude_x10":          latitude,
                   "longitude_x10":         longitude}

print(data_for_loxone)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.sendto(bytes(str(data_for_loxone), "utf-8"), (miniserver_ip, miniserver_port))
