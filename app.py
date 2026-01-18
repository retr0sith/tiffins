from fastapi import FastAPI, HTTPException
from zigbee.mock_adapter import MockZigbeeAdapter
from zigbee.clusters import CLUSTER_NAMES
from fastapi.staticfiles import StaticFiles
from zeroconf import Zeroconf, ServiceBrowser
import time


app = FastAPI(title="EthoHub Zigbee Bridge (Simulated)")

zigbee = MockZigbeeAdapter()

app.mount("/", StaticFiles(directory="static", html=True), name="static")
@app.on_event("startup")
async def startup():
    await zigbee.start()

@app.get("/zigbee/devices")
async def list_devices():
    return await zigbee.get_devices()

@app.post("/zigbee/command")
async def send_command(payload: dict):
    ieee = payload.get("ieee")
    cluster = payload.get("cluster")
    command = payload.get("command")

    if not await zigbee.send_command(ieee, cluster, command):
        raise HTTPException(400, "Command failed")

    return {"status": "ok"}
class MDNSListener:
    def __init__(self):
        self.devices = []

    def add_service(self, zeroconf, service_type, name):
        info = zeroconf.get_service_info(service_type, name)
        if info:
            device = {
                "name": name,
                "address": info.parsed_addresses()[0] if info.parsed_addresses() else None,
                "port": info.port,
                "type": service_type
            }
            if device not in self.devices:
                self.devices.append(device)
@app.post("/wifi/scan")
async def wifi_scan():
    zeroconf = Zeroconf()
    listener = MDNSListener()

    ServiceBrowser(
        zeroconf,
        "_services._dns-sd._udp.local.",
        listener
    )

    time.sleep(5)  # simple scan window
    zeroconf.close()

    return {
        "protocol": "wifi",
        "device_count": len(listener.devices),
        "devices": listener.devices
    }

@app.get("/")
def root():
    return {"status": "Zigbee simulation running"}
