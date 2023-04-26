from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import CommentOnProperty, HostReply, CommentOnReply, CommentOnUser


class PropertyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentOnProperty
        fields = "__all__"
        read_only_fields = ["id", "reservation", "created_at"]


class HostReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = HostReply
        fields = "__all__"
        read_only_fields = ["id", "comment", "created_at"]


class CommentOnReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentOnReply
        fields = "__all__"
        read_only_fields = ["id", "reply", "created_at"]


class CommentOnUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentOnUser
        fields = "__all__"
        read_only_fields = ["id", "reservation", "user", "created_at"]
