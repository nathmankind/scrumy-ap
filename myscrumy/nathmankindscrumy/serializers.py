from rest_framework import serializers
from .models import ScrumyGoals, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'id')


class ScrumUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrumyGoals
        fields = ('user', 'goal_name')


class ScrumGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrumyGoals
        fields = ('goal_name', 'goal_status', 'goal_id', 'created_by', 'moved_by', 'owner')
