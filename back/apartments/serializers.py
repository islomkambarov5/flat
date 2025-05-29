from rest_framework import serializers
from rest_framework.serializers import HiddenField, CurrentUserDefault
from .models import *


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image

        fields = ['image']


class CommentSerializer(serializers.ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['comment', 'user']


class FlatSerializer(serializers.ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    images = ImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Flat
        fields = [
            'user',
            'description',
            'phone_number',
            'name',
            'address',
            'city',
            'people',
            'room_count',
            'price_per_person',
            'status',
            'has_wifi',
            'has_ac',
            'has_contract',
            'images',
            'comments',

        ]
