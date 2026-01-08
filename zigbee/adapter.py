from abc import ABC, abstractmethod

class ZigbeeAdapter(ABC):

    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def get_devices(self):
        pass

    @abstractmethod
    async def send_command(self, ieee, cluster, command):
        pass

