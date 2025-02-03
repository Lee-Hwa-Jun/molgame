# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_name = self.scope['url_route']['kwargs']['game']
        self.room_name = self.scope['url_route']['kwargs']['room']
        self.room_group_name = f"{self.game_name}_{self.room_name}"

        # WebSocket 연결 수락
        await self.channel_layer.group_add(
            self.room_group_name,  # group에 추가
            self.channel_name,  # 현재 WebSocket 채널 이름
        )
        await self.accept()  # 연결 수락

    async def disconnect(self, close_code):
        # WebSocket 연결 종료 시 호출
        await self.channel_layer.group_discard(
            self.room_group_name,  # 그룹에서 제거
            self.channel_name,
        )

    # 클라이언트로부터 메시지가 오면 이 메서드가 실행
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)  # 받은 데이터는 JSON 포맷
        data = text_data_json['message']  # 예시로 'move' 데이터 추출

        # 다른 모든 사용자에게 메시지 전달
        await self.channel_layer.group_send(
            self.room_group_name,  # 메시지를 보낼 그룹
            {
                'type': 'message',  # 이 메시지를 처리할 메서드 이름
                'data': data,
            }
        )

    # 그룹에서 받은 메시지를 클라이언트에 전달
    async def message(self, event):
        data = event['data']

        # 클라이언트로 메시지 전달
        await self.send(text_data=json.dumps({
            'message': data,  # 클라이언트로 보낼 데이터
        }))
