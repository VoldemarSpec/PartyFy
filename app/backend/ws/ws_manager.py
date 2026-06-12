from collections import defaultdict
from fastapi import WebSocket
import json

class WSManager:
    def __init__(self):
        self.rooms: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, party_uuid: str, websocket: WebSocket):
        await websocket.accept()
        self.rooms[party_uuid].add(websocket)

    def disconnect(self, party_uuid: str, websocket: WebSocket):
        if party_uuid in self.rooms:
            self.rooms[party_uuid].discard(websocket)
            if not self.rooms[party_uuid]:
                del self.rooms[party_uuid]

    async def broadcast_to_party(self, party_uuid: str, message: dict):
        dead = []
        for ws in self.rooms.get(party_uuid, set()):
            try:
                await ws.send_text(json.dumps(message))
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(party_uuid, ws)

ws_manager = WSManager()
