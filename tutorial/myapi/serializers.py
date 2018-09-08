from rest_framework import serializers
from myapi.models import Student


class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=False, allow_blank=True, max_length=100)
    joining_date = serializers.DateTimeField(required=False)
    course = serializers.CharField(
        required=False, allow_blank=True, max_length=100)
    department = serializers.CharField(
        required=False, allow_blank=True, max_length=100)

    def create(self, validated_data):
        return Student.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.joining_date = validated_data.get(
            'joining_date', instance.joining_date)
        instance.course = validated_data.get(
            'course', instance.course)
        instance.department = validated_data.get(
            'department', instance.department)
        instance.save()
        return instance
