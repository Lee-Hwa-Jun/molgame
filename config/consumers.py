from channels.generic.websocket import AsyncWebsocketConsumer
import uuid, os, redis, json
from dotenv import load_dotenv

load_dotenv()
redis_client = redis.Redis(
    host=os.getenv("REDIS_IP", "redis"),  # 기본값 'redis' (Docker Compose)
    port=6379,
    db=0,
    password=os.getenv("REDIS_PASSWORD")
)

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room']
        self.room_group_name = f"omok_{self.room_name}"
        self.user_id = str(uuid.uuid4())  # 고유 사용자 ID 생성
        self.role = None

        room_key = f"room_{self.room_name}"
        room_data = redis_client.hgetall(room_key)

        if not room_data:
            # 방 생성: 흑
            redis_client.hset(room_key, mapping={
                'creator': self.user_id,
                'players': json.dumps([self.user_id]),  # JSON 문자열로 저장
                'black': self.user_id,
                'white': ''  # 백 플레이어는 아직 없음
            })
            self.role = 'black'
        else:
            # 방 데이터에서 players 키 처리
            players_bytes = room_data.get(b'players')  # bytes로 반환
            if players_bytes:
                # bytes를 문자열로 변환하고, 이스케이프 문제 해결
                players_str = players_bytes.decode('utf-8')
                # 이중 이스케이프 문제 방지: JSON 파싱 전 이스케이프 제거
                try:
                    players = json.loads(players_str)
                except json.JSONDecodeError:
                    # 이스케이프 문자 제거 후 재시도
                    players = json.loads(players_str.replace('\\"', '"'))
            else:
                players = []  # players 키가 없으면 빈 리스트로 초기화

            if len(players) < 2:
                # 방 입장: 백
                players.append(self.user_id)
                redis_client.hset(room_key, mapping={
                    'players': json.dumps(players),  # JSON 문자열로 저장
                    'white': self.user_id
                })
                self.role = 'white'
            else:
                await self.close()
                return

        redis_client.hset(f"user_{self.user_id}", 'role', self.role)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # 역할 및 초기 상태 전송
        await self.send(text_data=json.dumps({
            'type': 'role',
            'message': {'role': self.role, 'user_id': self.user_id}
        }))
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'game_status',
            'message': {'current_turn': 'black'}
        })

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        # 접속 끊김 알림
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'player_disconnect',
            'message': {'user_id': self.user_id}
        })

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        if data['type'] == 'move':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'game_move',
                'message': message
            })
        elif data['type'] == 'chat':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'message': message
            })
        elif data['type'] == 'ping':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'pong',
                'message': {'user_id': self.user_id}
            })

    async def game_move(self, event):
        await self.send(text_data=json.dumps({'type': 'move', 'message': event['message']}))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({'type': 'chat', 'message': event['message']}))

    async def game_status(self, event):
        await self.send(text_data=json.dumps({'type': 'status', 'message': event['message']}))

    async def pong(self, event):
        await self.send(text_data=json.dumps({'type': 'pong', 'message': event['message']}))

    async def player_disconnect(self, event):
        await self.send(text_data=json.dumps({'type': 'disconnect', 'message': event['message']}))

class LobbyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    class LobbyConsumer(AsyncWebsocketConsumer):
        async def connect(self):
            await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'get_rooms':
            rooms = redis_client.keys('room_*')
            room_list = []
            for r in rooms:
                players_bytes = redis_client.hget(r, b'players')
                if players_bytes:
                    try:
                        players_str = players_bytes.decode('utf-8')
                        players = json.loads(players_str.replace('\\"', '"'))
                        room_list.append({'name': r.decode('utf-8')[5:], 'players': len(players)})
                    except json.JSONDecodeError:
                        continue  # 파싱 실패 시 건너뜀
            await self.send(text_data=json.dumps({'type': 'room_list', 'message': {'rooms': room_list}}))
        elif data['type'] == 'create_room':
            room_name = data['message'].get('name', '').strip()
            if not room_name:
                await self.send(text_data=json.dumps({
                    'type': 'room_error',
                    'message': {'error': '방 이름을 입력하세요.'}
                }))
                return

            # room_* 패턴으로 방 이름 확인
            room_key = f"room_{room_name}"
            if redis_client.exists(room_key):
                await self.send(text_data=json.dumps({
                    'type': 'room_error',
                    'message': {'error': '이미 방이 존재합니다.'}
                }))
            else:
                await self.send(text_data=json.dumps({
                    'type': 'room_created',
                    'message': {'name': room_name}
                }))