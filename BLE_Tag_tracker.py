import asyncio
from bleak import BleakScanner

# A dictionary to store RSSI values for each detected iBeacon
rssi_history = {}

async def main():

    devices = await BleakScanner.discover(10.0, return_adv=True)
    for d in devices:
        raw_data = devices[d][1]
        manufacturer_id=raw_data.manufacturer_data

        # Check for iBeacon by Manufacturer ID (76)
        if 76 in manufacturer_id:  # Check if it's an iBeacon
            print(f"iBeacon detected")
            print(f"RSSI: {raw_data.rssi}")
            
           
        else:
            # Do nothing for non-iBeacon devices
            continue  # Skip to the next device

asyncio.run(main())
