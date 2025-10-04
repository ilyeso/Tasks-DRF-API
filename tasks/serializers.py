from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task


class UserSelializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class TaskSerializer(serializers.ModelSerializer):
    affected_to = UserSelializer(many = True, read_only = True)
    affected_to_ids = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        many = True,
        write_only = True,
        source = 'affected_to'
    )

    class Meta:
        model = Task
        fields = [
            'id', 'label' , 'description' , 'affected_to' , 'affected_to_ids', 'type', 'priority',
            # 'attached_file', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_priority(self,value):
        if value < 1 or value > 5 :
            raise serializers.ValidationError("Priority must be between 1 and 5 ")
        return value
    
    def validate_attached_file(self,value):
        if value and not value.name.endswith('.pdf'):
            raise serializers.ValidationError("File not allowed, only PDF !")
        return value