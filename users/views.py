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
        serializer = UserSerializer(request.user)  # Serializa o usuário autenticado
        return Response({
            'user':serializer.data,
            'token': {
                'exp': self.convert_timestamp(request.auth['exp']),
                'iat': self.convert_timestamp(request.auth['iat'])
            }
            })
        
    def convert_timestamp(self, timestamp:float):
        return datetime.fromtimestamp(timestamp=timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')