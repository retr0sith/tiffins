from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from zigbee.mock_adapter import MockZigbeeAdapter

app = FastAPI(title="EthoHub Zigbee Simulator")

zigbee = MockZigbeeAdapter()

app.mount("/ui", StaticFiles(directory="static", html=True), name="static")

@app.on_event("startup")
async def startup():
    await zigbee.start()

@app.get("/zigbee/scan")
async def scan_devices():
    return await zigbee.scan()

@app.post("/zigbee/toggle")
async def toggle_device(payload: dict):
    ieee = payload.get("ieee")
    value = payload.get("value")

    if not await zigbee.toggle(ieee, value):
        raise HTTPException(400, "Device not found")

    return {"status": "ok"}
