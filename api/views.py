import jwt
import datetime
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from .serializers import UserSerializer

User = get_user_model()

JWT_EXP_DELTA_SECONDS = 60 * 60 * 24 * 7  # 7 days

def create_token_for_user(user):
    payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    # PyJWT returns bytes in older versions; ensure string
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

@api_view(['POST'])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email", "")
    if not username or not password:
        return Response({"error": "username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    # default role already set in model; adjust if needed
    token = create_token_for_user(user)
    return Response({"token": token, "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({"error": "username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    token = create_token_for_user(user)
    return Response({"token": token, "user": UserSerializer(user).data}, status=status.HTTP_200_OK)
