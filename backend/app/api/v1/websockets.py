from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import redis.asyncio as redis
import json

from app.core.config import settings

router = APIRouter()


@router.websocket("/v1/ws/resumes/{resume_id}")
async def resume_status_ws(websocket: WebSocket, resume_id: str):
    await websocket.accept()

    redis_client = redis.from_url(settings.REDIS_URL)
    pubsub = redis_client.pubsub()
    channel_name = f"resume_status:{resume_id}"
    await pubsub.subscribe(channel_name)

    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                await websocket.send_json(data)

                if data.get("status") in ("completed", "failed"):
                    break

    except WebSocketDisconnect:
        pass

    finally:
        await pubsub.unsubscribe(channel_name)
        await pubsub.close()
        await redis_client.close()
        try:
            await websocket.close()
        except Exception:
            pass