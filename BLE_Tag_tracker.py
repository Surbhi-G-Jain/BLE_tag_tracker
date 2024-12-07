import asyncio
from bleak import BleakScanner
import collections

rssi_vals =collections.deque(maxlen=10)
async def main():
    
    while True:

        devices = await BleakScanner.discover(2.0, return_adv=True)
        for d in devices:
            raw_data = devices[d][1]
            manufacturer_id=raw_data.manufacturer_data

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
                pass

asyncio.run(main())
