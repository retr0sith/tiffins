import uuid
from zigbee.clusters import ON_OFF, LEVEL_CONTROL, MOTION

def simulated_devices():
    return [
        {
            "ieee": str(uuid.uuid4()),
            "name": "Simulated Smart Light",
            "clusters": {
                ON_OFF: {"state": False},
                LEVEL_CONTROL: {"brightness": 128}
            }
        },
        {
            "ieee": str(uuid.uuid4()),
            "name": "Simulated Motion Sensor",
            "clusters": {
                MOTION: {"motion": False}
            }
        }
    ]
