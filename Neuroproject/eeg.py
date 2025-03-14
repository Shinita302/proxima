import numpy as np
import serial
import time
import ctypes
import thinkgear

# Load ThinkGear DLL (ensure that ThinkGear.dll is in the same directory or provide full path)
try:
    thinkgear = ctypes.CDLL("ThinkGear.dll")
except OSError as e:
    print(f"Error loading DLL: {e}")
    exit()

# Initialize the ThinkGear device
try:
    thinkgear.TG_Connect.restype = ctypes.c_int  # Set the return type of TG_Connect
    thinkgear.TG_Connect.argtypes = []  # Set argument types for TG_Connect
except AttributeError:
    print("Failed to set up ThinkGear function signatures.")
    exit()

# Set up the serial port (make sure the COM port is correct)
try:
    ser = serial.Serial("COM3", baudrate=9600)  # Replace "COM3" with your actual COM port
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

# Initialize ThinkGear connection
if thinkgear.TG_Connect() != 0:
    print("Failed to connect to the ThinkGear device.")
    ser.close()
    exit()

print("Successfully connected to the ThinkGear device.")

# Read data from the NeuroSky device
try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()  # Decode byte data to string and remove extra spaces
            print(data)  # Print the raw data received from the device
            
        time.sleep(0.1)  # Adjust the sleep time to balance performance and data reading speed

except KeyboardInterrupt:
    print("Exiting program.")

finally:
    # Close the serial port and disconnect the ThinkGear device properly
    ser.close()
    try:
        thinkgear.TG_Disconnect()  # Assuming TG_Disconnect exists in the ThinkGear DLL
        print("Disconnected from the device.")
    except AttributeError:
        print("Failed to disconnect from the device properly.")

        