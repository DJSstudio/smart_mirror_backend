import jwt
import datetime
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

JWT_EXP_DELTA_SECONDS = 60 * 60 * 24 * 7  # 7 days

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# def create_token_for_user(user):
#     payload = {
#         "user_id": user.id,
#         "username": user.username,
#         "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
#     }
#     token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
#     # PyJWT returns bytes in older versions; ensure string
#     if isinstance(token, bytes):
#         token = token.decode('utf-8')
#     return token

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
    token = get_tokens_for_user(user)
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

    token = get_tokens_for_user(user)
    return Response({"token": token, "user": UserSerializer(user).data}, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "You are authenticated!"})

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_me(request):
    user = request.user
    username = request.data.get("username", user.username)
    bio = request.data.get("bio", user.bio if hasattr(user, "bio") else "")

    # prevent duplicate username
    if User.objects.exclude(id=user.id).filter(username=username).exists():
        return Response({"error": "username already taken"}, status=400)

    user.username = username

    # if your User model has bio field
    if hasattr(user, "bio"):
        user.bio = bio

    user.save()

    return Response(UserSerializer(user).data, status=200)
