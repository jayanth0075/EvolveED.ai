# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProgress


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm', 'role',
                  'phone', 'current_education', 'current_job', 'skills', 'interests']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        UserProgress.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password')

        return attrs


class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    progress = UserProgressSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role', 'phone', 'date_of_birth',
                  'profile_picture', 'bio', 'current_education', 'current_job',
                  'skills', 'interests', 'total_quizzes_taken', 'total_notes_generated',
                  'current_level', 'created_at', 'progress']
        read_only_fields = ['id', 'email', 'created_at', 'total_quizzes_taken',
                            'total_notes_generated']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone', 'date_of_birth', 'profile_picture', 'bio',
                  'current_education', 'current_job', 'skills', 'interests']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs