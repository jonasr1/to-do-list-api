from datetime import datetime, timezone
from typing import Any, Dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed
from core import settings
from users.models import User
from users.serializers import UserSerializer
import jwt

class RegisterView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=201)
    

class UserView(APIView):
    def get(self, request: Request) -> Response:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer'):
            raise AuthenticationFailed('Token not provided!')
        token = auth_header.split(' ')[1]
        payload = self.decode_token(token)
        user = User.objects.filter(id=payload['user_id']).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        return Response({
            'user': {
                'user_id': user.id,
                'username': user.username,
                'is_active': user.is_active,
            },
            'token': {
                'token_type': payload['token_type'],
                'exp': self.convert_timestamp(payload['exp']),
                'iat': self.convert_timestamp(payload['iat'])
            }
        })
        
    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(
                jwt=token,
                key=settings.SIMPLE_JWT['SIGNING_KEY'],
                algorithms=settings.SIMPLE_JWT['ALGORITHM']
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
    
    def convert_timestamp(self, timestamp:float):
        return datetime.fromtimestamp(timestamp=timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')