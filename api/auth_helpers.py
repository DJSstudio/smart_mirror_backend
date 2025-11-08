import jwt
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

def user_from_token(request):
    auth = request.META.get('HTTP_AUTHORIZATION', '')
    if not auth.startswith('Bearer '):
        return None
    token = auth.split(' ')[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('user_id')
        return User.objects.filter(id=user_id).first()
    except Exception:
        return None

@api_view(['GET'])
def protected_view(request):
    user = user_from_token(request)
    if user is None:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({"message": f"Hello {user.username}"})
