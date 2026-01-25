import asyncio

class MockZigbeeAdapter:
    def __init__(self):
        self.devices = [
            {
                "ieee": "00:11:22:33:44:55:01",
                "name": "Living Room Light",
                "type": "light",
                "state": False
            },
            {
                "ieee": "00:11:22:33:44:55:02",
                "name": "Bedroom Light",
                "type": "light",
                "state": False
            }
        ]

    async def start(self):
        # Simulate Zigbee network forming
        await asyncio.sleep(1)

    async def scan(self):
        # Simulated scan delay
        await asyncio.sleep(1)
        return self.devices

    async def toggle(self, ieee, value):
        for d in self.devices:
            if d["ieee"] == ieee:
                d["state"] = value
                return True
        return False

