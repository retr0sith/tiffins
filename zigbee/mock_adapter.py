import asyncio
from zigbee.adapter import ZigbeeAdapter
from zigbee.devices import simulated_devices
from zigbee.clusters import ON_OFF

class MockZigbeeAdapter(ZigbeeAdapter):

    def __init__(self):
        self.devices = simulated_devices()

    async def start(self):
        print("[ZIGBEE-MOCK] Zigbee network started (SIMULATED)")

        # Background task: simulate motion events
        asyncio.create_task(self._simulate_motion())

    async def get_devices(self):
        return self.devices

    async def send_command(self, ieee, cluster, command):
        for dev in self.devices:
            if dev["ieee"] == ieee:
                if cluster == ON_OFF:
                    dev["clusters"][ON_OFF]["state"] = command == "on"
                    print(f"[ZIGBEE-MOCK] {dev['name']} → {command.upper()}")
                    return True
        return False

    async def _simulate_motion(self):
        while True:
            for dev in self.devices:
                if "Motion" in dev["name"]:
                    dev["clusters"][0x0500]["motion"] = True
                    print("[ZIGBEE-MOCK] Motion detected")
                    await asyncio.sleep(3)
                    dev["clusters"][0x0500]["motion"] = False
            await asyncio.sleep(10)
