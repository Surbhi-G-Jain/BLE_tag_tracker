import asyncio
from bleak import BleakScanner
import collections

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


                        
                        else:
                            print("I beacon not found")
                    else:
                        print("No manufacturer id found")

                except Exception as e:
                    print(f"Unexpected error with device {d.name}: {e}")


        except asyncio.CancelledError:
            print("Scan cancelled.")
            break  # Exit the loop if the scan is cancelled
        except Exception as e:
            print(f"Error during device scanning: {e}")

asyncio.run(main())
