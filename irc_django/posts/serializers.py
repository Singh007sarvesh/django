from rest_framework import serializers
from posts.models import Channel, Message
from django.contrib.auth.models import User





class MessageSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # message = serializers.CharField(
    #     required=False, allow_blank=True, max_length=100)
    # creator = serializers.CharField(read_only=True)
    # channel = serializers.CharField(read_only=True)
    # created_at = serializers.DateTimeField(required=False)

    # def create(self, validated_data):
    #     return Message.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.message = validated_data.get('message', instance.message)
    #     instance.created_at = validated_data.get(
    #         'created_at', instance.created_at)
    #     instance.channel = validated_data.get(
    #         'channel', instance.channel)
    #     instance.creator = validated_data.get('creator', instance.creator)
    #     instance.save()
    #     return instance
    class Meta:
        model = Message
        fields = ('__all__')


class ChannelSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=False, allow_blank=True, max_length=100)

    messages = MessageSerializer(many=True)

    def create(self, validated_data):
       # return Channel.objects.create(**validated_data)
       #import pdb; pdb.set_trace()
       messages = validated_data.pop('messages')
       channel= Channel.objects.create(**validated_data)
       i=1
       for msg in messages:
        message = msg['message']
        creator = msg['creator']
        print(message)
        print(creator)
        Message.objects.create(message=message, creator=creator, channel=channel)
        i=i+1
       return channel

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')
