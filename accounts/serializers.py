from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    theme_primary_color = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'nome', 'cpf', 'telefone', 'email', 'cargo', 'is_active', 'is_dizimista', 'password', 'theme_primary_color']
        read_only_fields = ['id']

    def get_theme_primary_color(self, obj):
        try:
            return obj.profile.theme_primary_color
        except Exception:
            return '#6750A4'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = super().create(validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField()

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError('Nova senha e confirmação não conferem')
        return data
