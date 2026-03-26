from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'telegram_chat_id', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации по email"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password_confirm')

    def validate_email(self, value):
        """Проверка уникальности email"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

    def validate(self, data):
        """Проверка совпадения паролей"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Пароли не совпадают"})

        # Если username не указан, используем часть email
        if not data.get('username'):
            data['username'] = data['email'].split('@')[0]

        return data

    def create(self, validated_data):
        """Создание пользователя"""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username', ''),
            password=validated_data['password']
        )
        return user


class CustomTokenObtainPairSerializer(serializers.Serializer):
    """ Кастомный сериализатор для получения JWT токена по email. """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError(
                "Необходимо указать email и пароль"
            )

        # Аутентификация по email
        from django.contrib.auth import authenticate
        user = authenticate(request=self.context.get('request'),
                            username=email, password=password)

        if not user:
            raise serializers.ValidationError(
                "Неверный email или пароль"
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "Учетная запись неактивна"
            )

        # Генерируем токены
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }


class EmailLoginSerializer(serializers.Serializer):
    """Сериализатор для входа по email"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)