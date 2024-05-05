from window_gui import create_window_gui
import serial
ROBOT_CONNECTED = True

arduino = None
if ROBOT_CONNECTED:
    arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

# Call the function to run the button GUI
create_window_gui(arduino)
