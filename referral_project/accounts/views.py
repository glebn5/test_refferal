from django.shortcuts import render
import random
import time
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import PhoneNumberSerializer, VerifyCodeSerializer, ProfileSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = ProfileSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def activate_invite_code(request):
    code = request.data.get('code')
    if not code:
        return Response({'detail': 'Код обязателен'}, status=400)

    user = request.user
    if user.target_invite_code:
        return Response({'detail': 'Вы уже активировали код ранее'}, status=400)

    try:
        inviter = User.objects.get(self_invite_code=code)
    except User.DoesNotExist:
        return Response({'detail': 'Неверный инвайт-код'}, status=404)

    if inviter == user:
        return Response({'detail': 'Нельзя активировать свой собственный код'}, status=400)

    user.target_invite_code = code
    user.invited_by = inviter
    user.save()

    return Response({'detail': 'Инвайт-код успешно активирован'})



class SendCodeView(APIView):
    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            code = str(random.randint(1000, 9999))
            cache.set(f'verify_code_{phone}', code, timeout=300)
            print(f"[DEBUG] Sending code {code} to {phone}")

            time.sleep(1.5)
            return Response({"detail": "Код отправлен (эмуляция)", "code": code}, status=200)

        return Response(serializer.errors, status=400)


class VerifyCodeView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']
            real_code = cache.get(f'verify_code_{phone}')

            if real_code == code:
                user, created = User.objects.get_or_create(phone_number=phone)
                user.is_verified = True
                user.is_active = True
                user.save()

                refresh = RefreshToken.for_user(user)

                return Response({
                        "detail": "Пользователь подтверждён",
                        "is_new": created,
                        "invite_code": user.self_invite_code,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }, status=200)
            return Response({"detail": "Неверный код"}, status=400)
        return Response(serializer.errors, status=400)