from fastapi import FastAPI, HTTPException
from zigbee.mock_adapter import MockZigbeeAdapter
from zigbee.clusters import CLUSTER_NAMES
from fastapi.staticfiles import StaticFiles



app = FastAPI(title="EthoHub Zigbee Bridge (Simulated)")
app.mount("/", StaticFiles(directory="static", html=True), name="static")
zigbee = MockZigbeeAdapter()


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

@app.get("/")
def root():
    return {"status": "Zigbee simulation running"}
