from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserSerializer

class RegisterView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=201)
    

class UserView(APIView):
    permission_classes = [IsAuthenticated] # Garante que a requisição precise de autenticação
    def get(self, request: Request) -> Response:
        user = request.user  # O usuário é automaticamente extraído da requisição pelo SimpleJWT
        return Response({
            'user': {
                'user_id': user.id,
                'username': user.username,
                'is_active': user.is_active,
            },
            'token': {
                'token_type': request.auth['token_type'],
                'exp': self.convert_timestamp(request.auth['exp']),
                'iat': self.convert_timestamp(request.auth['iat'])
            }
        })
        
    def convert_timestamp(self, timestamp:float):
        return datetime.fromtimestamp(timestamp=timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')