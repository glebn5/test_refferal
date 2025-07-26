from rest_framework import serializers
from .models import User


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)

class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=4)



class ProfileSerializer(serializers.ModelSerializer):
    invite_code = serializers.CharField(source='self_invite_code', read_only=True)
    activated_invite_code = serializers.CharField(source='target_invite_code', read_only=True, allow_blank=True)
    invited_by = serializers.SerializerMethodField()
    referrals = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['phone_number', 'invite_code', 'activated_invite_code', 'invited_by', 'referrals']

    def get_invited_by(self, obj):
        if obj.invited_by:
            return obj.invited_by.phone_number
        return None

    def get_referrals(self, obj):
        return [user.phone_number for user in obj.referrals.all()]
