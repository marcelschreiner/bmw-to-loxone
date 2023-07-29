# bmw-to-loxone
A python script to send state information of BMW cars to Loxone Miniserver.
Execute this script every few minutes. The script does only poll the BMW server once and quits again.

## Example on Raspberry Pi

Let's say the script is run on a Raspberry Pi. To execute it every 30min the following config needs to be made:

- In the terminal enter: "crontab -e"
- Then add the line "*/30 * * * * python3 /home/pi/bmw2lox.py"
- Save and exit
