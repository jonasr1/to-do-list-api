from datetime import datetime
from zoneinfo import ZoneInfo

from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer


class RegisterView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User registered successfully"}, status=201)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        serializer = UserSerializer(request.user)
        token = request.auth
        exp = getattr(token, "payload", {}).get("exp")
        iat = getattr(token, "payload", {}).get("iat")
        return Response({
            "user": serializer.data,
            "token": {
                "exp": self.convert_timestamp(exp) if exp else None,
                "iat": self.convert_timestamp(iat) if iat else None,
            },
        })

    def convert_timestamp(self, timestamp: float) -> str:
        return datetime.fromtimestamp(
            timestamp=timestamp, tz=ZoneInfo("America/Sao_Paulo")
        ).strftime("%d/%m/%y %H:%M:%S")
