import json
from collections import defaultdict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["realtime"])


class ConnectionManager:
    def __init__(self) -> None:
        self.rooms: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, room: str, socket: WebSocket) -> None:
        await socket.accept()
        self.rooms[room].append(socket)

    def disconnect(self, room: str, socket: WebSocket) -> None:
        self.rooms[room] = [conn for conn in self.rooms[room] if conn != socket]

    async def broadcast(self, room: str, message: dict) -> None:
        payload = json.dumps(message)
        for connection in self.rooms[room]:
            await connection.send_text(payload)


manager = ConnectionManager()


@router.websocket("/ws/review/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str) -> None:
    await manager.connect(room, websocket)
    await manager.broadcast(room, {"type": "status", "message": "A reviewer joined"})

    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(room, {"type": "comment", "payload": data})
    except WebSocketDisconnect:
        manager.disconnect(room, websocket)
        await manager.broadcast(room, {"type": "status", "message": "A reviewer left"})
