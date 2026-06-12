from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.backend.ws.ws_manager import ws_manager

router = APIRouter()

@router.websocket("/ws/items/{party_uuid}")
async def items_ws(websocket: WebSocket, party_uuid: str):
    await ws_manager.connect(party_uuid, websocket)
    try:
        while True:
            # держим соединение живым; можно читать ping/pong от клиента
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(party_uuid, websocket)
    except Exception:
        ws_manager.disconnect(party_uuid, websocket)
