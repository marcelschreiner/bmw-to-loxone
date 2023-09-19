# BMW to Loxone Bridge

This Python script establishes a bridge between your BMW vehicle and a Loxone Miniserver, allowing you to monitor various aspects of your BMW remotely and send relevant data to the Loxone system. The script retrieves information from your BMW, such as door lock status, charging status, and location, and then sends this data to your Loxone Miniserver over UDP.

## Prerequisites

Before you can use this script, you'll need the following:

- Python 3
- The `bimmer-connected` library
- Access to a BMW ConnectedDrive account
- Access to a Loxone Miniserver

## Setup

1. Install the required Python packages using `pip`:
  (`pip3` is traditionally used on Rapberry Pis to install libraries for Python 3 other systems may use `pip`)

   ```shell
   pip3 install bimmer-connected
   ```

3. Modify the script to include your BMW and Loxone Miniserver information:

   ```python
   # BMW login data
   USERNAME = 'some@email.com'
   PASSWORD = 'YourSuperSecurePassword'
   VIN = 'VinOfYourCar'
   
   # Loxone Miniserver IP and UDP target port
   MINISERVER_IP = "192.168.1.30"
   MINISERVER_PORT = 1234
   ```

   Replace `'your@email.com'`, `'your_super_secure_password'`, and `'VIN_OF_YOUR_CAR'` with your BMW ConnectedDrive account credentials and your BMW's VIN (Vehicle Identification Number). Adjust the `miniserver_ip` and `miniserver_port` to match your Loxone Miniserver configuration.

## Usage

Run the script to retrieve data from your BMW and send it to your Loxone Miniserver:

```shell
python3 bmw2lox.py
```

The script will print the collected data to the console and send it to the specified Loxone Miniserver. The script only polls the BMW server once and quits again. To execute it every few minutes you can use cron. Keep in mind that the BMW server has a low max polling rate! The following example is for a Raspberry Pi to run the script every 30min:

```shell
- In the terminal enter: "crontab -e"
- Then add the line "*/30 * * * * python3 /home/pi/bmw2lox.py"
- Save and exit
```

## Data Sent to Loxone

The script collects the following data from your BMW and sends it to the Loxone Miniserver:

- `all_lids_closed`: Indicates whether all lids (doors, trunk, etc.) are closed.
- `all_windows_closed`: Indicates whether all windows are closed.
- `car_locked`: Indicates whether the car is locked (1 for locked, 0 for unlocked).
- `charging_level_hv`: The remaining battery charge percentage.
- `is_charger_connected`: Indicates whether the charger is connected to the vehicle.
- `is_charging`: Indicates whether the vehicle is currently charging (1 for charging, 0 otherwise).
- `latitude_x10` and `longitude_x10`: The latitude and longitude of the vehicle's location, multiplied by 10 for compatibility with Loxone.

Please note that some data fields are commented out in the script. You can uncomment and modify these fields to include additional information if needed.

## License

This script is provided under the [MIT License](LICENSE.md). Feel free to modify and use it according to your needs.
