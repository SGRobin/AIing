from window_gui import create_window_gui
import serial
ROBOT_CONNECTED = True


arduino = None
if ROBOT_CONNECTED:
    try:
        arduino = serial.Serial(port='COM3', baudrate=9600, timeout=2, exclusive=True)

        # Call the function to run the button GUI
        create_window_gui(arduino)
    finally:
        #arduino.close()
        pass
