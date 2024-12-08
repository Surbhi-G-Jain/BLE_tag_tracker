import asyncio
from bleak import BleakScanner
import collections
import platform
import math


def fixed_point_to_float(value):
    if value & 0x8000:  # converting Negative number in two's complement
        value -= 0x10000
    return value / 256.0

rssi_vals =collections.deque(maxlen=10)
async def main():
    
    while True:

        try:

            devices = await BleakScanner.discover(2.0, return_adv=True)

            if not devices:
                print("No devices found")
                continue

            for d in devices:
                try:
                    raw_data = devices[d][1]
                    print(raw_data)
                    manufacturer_id=raw_data.manufacturer_data
                    if manufacturer_id:
                    # Check for manufacturer id for i beacon
                        if 76 in manufacturer_id:
                            #print(f"iBeacon detected")
                            #print(f"RSSI: {raw_data.rssi}")
                            current_rssi = raw_data.rssi
                            rssi_vals.append(current_rssi)
                            
                            if len(rssi_vals) == 10:  # Only process after we have enough data
                                avg_rssi = sum(rssi_vals) / 10

                                if current_rssi > avg_rssi + 10 or current_rssi < avg_rssi - 10:
                                    print("iBeacon is moving")
                                    
                                else:
                                    print("iBeacon seems stationary.")

                    elif 0xE1FF in manufacturer_id:  

                        x_raw_val = int(raw_data[28:32], 16)  # Extract X-axis data
                        y_raw_val = int(raw_data[32:36], 16)  # Extract Y-axis data
                        z_raw_val = int(raw_data[36:40], 16)  # Extract Z-axis data

                        # Convert to floating-point values
                        x = fixed_point_to_float(x_raw_val)
                        y = fixed_point_to_float(y_raw_val)
                        z = fixed_point_to_float(z_raw_val)


                        magnitude = math.sqrt(x**2 + y**2 + z**2)

                    
                        threshold = 0.1

                        # checking if accelerometer is moving or stationary
                        if magnitude > threshold:
                            print(f"Moving: Magnitude = {magnitude:.2f}")
                        else:
                            print(f"Stationary: Magnitude = {magnitude:.2f}")

                        
                    
                    else:
                        print("No manufacturer id found")

                except Exception as e:
                    print(f"Unexpected error with device {d.name}: {e}")


        except asyncio.CancelledError:
            print("Scan cancelled.")
            if platform.system() == "Windows":
                print("Ensure Bluetooth support is enabled via WinRT.")
            elif platform.system() == "Linux":
                print("Ensure 'bluez' and 'dbus' are installed.")
            elif platform.system() == "Darwin":
                print("Ensure CoreBluetooth is functioning.")


            break  # Exit the loop if the scan is cancelled
        except Exception as e:
            print(f"Error during device scanning: {e}")

asyncio.run(main())
