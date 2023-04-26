from django.shortcuts import get_object_or_404, render
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from .models import CommentOnProperty, HostReply, CommentOnReply, CommentOnUser
from .serializers import (
    PropertyCommentSerializer,
    HostReplySerializer,
    CommentOnReplySerializer,
    CommentOnUserSerializer,
)
from reservations.models import Reservation
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import serializers
from user.models import User
from properties.models import Property
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.paginator import Paginator


class CustomPagination(PageNumberPagination):
    page_size = 1

    def get_paginated_response(self, data):
        return Response(data)


class PropertyCommentCreateView(CreateAPIView):
    serializer_class = PropertyCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        property_id = self.kwargs["property_id"]
        reservation_id = self.kwargs["reservation_id"]
        return CommentOnProperty.objects.filter(
            reservation_id=reservation_id, reservation__property_id=property_id
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        reservation = get_object_or_404(
            Reservation,
            pk=self.kwargs["reservation_id"],
            property_id=self.kwargs["property_id"],
        )
        context.update({"reservation": reservation})
        return context

    def perform_create(self, serializer):
        property_id = self.kwargs["property_id"]
        reservation_id = self.kwargs["reservation_id"]
        user = self.request.user
        reservation = get_object_or_404(
            Reservation, pk=reservation_id, property_id=property_id
        )
        if reservation.user != self.request.user:
            raise serializers.ValidationError(
                "You are not allowed to create this comment"
            )
        if CommentOnProperty.objects.filter(
            reservation=reservation, reservation__user=user
        ).exists():
            raise serializers.ValidationError(
                "You have already commented on this reservation"
            )
        if reservation.state not in ["Cm", "Tm"]:
            raise serializers.ValidationError("The reservation is not completed")
        serializer.save(reservation_id=reservation_id)


class PropertyCommentListView(ListAPIView):
    serializer_class = PropertyCommentSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self):
        property_id = self.kwargs["property_id"]
        comments = CommentOnProperty.objects.filter(
            reservation__property_id=property_id
        )
        return comments

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"show_replies": True})
        return context


class PropertyCommentReplyView(CreateAPIView):
    serializer_class = HostReplySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        comment = get_object_or_404(CommentOnProperty, pk=self.kwargs["comment_id"])
        property_id = comment.reservation.property.id
        return HostReply.objects.filter(comment__reservation__property_id=property_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        comment = get_object_or_404(CommentOnProperty, pk=self.kwargs["comment_id"])
        context.update({"comment": comment})
        return context

    def perform_create(self, serializer):
        comment_id = self.kwargs["comment_id"]
        user = self.request.user
        comment = get_object_or_404(CommentOnProperty, pk=self.kwargs["comment_id"])
        if comment.reservation.host != self.request.user:
            raise serializers.ValidationError(
                "You are not allowed to create this comment"
            )
        if HostReply.objects.filter(
            comment=comment, comment__reservation__host=user
        ).exists():
            raise serializers.ValidationError(
                "You have already replied on this comment"
            )
        serializer.save(comment_id=comment_id)


class PropertyCommentReplyListView(ListAPIView):
    serializer_class = HostReplySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        comment_id = self.kwargs["comment_id"]
        return HostReply.objects.filter(comment_id=comment_id)


class CommentOnReplyCreateView(CreateAPIView):
    serializer_class = CommentOnReplySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = CommentOnReply.objects.filter(
            reply_id=self.kwargs["reply_id"]
        ).order_by("id")
        paginator = Paginator(queryset, 1)
        page_number = self.request.query_params.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj

    def get_serializer_context(self):
        context = super().get_serializer_context()
        reply = get_object_or_404(HostReply, pk=self.kwargs["reply_id"])
        context.update({"reply": reply})
        return context

    def perform_create(self, serializer):
        reply_id = self.kwargs["reply_id"]
        user = self.request.user
        reply = get_object_or_404(HostReply, pk=self.kwargs["reply_id"])
        if reply.comment.reservation.user != self.request.user:
            raise serializers.ValidationError(
                "You are not allowed to create this comment"
            )
        if CommentOnReply.objects.filter(
            reply=reply, reply__comment__reservation__user=user
        ).exists():
            raise serializers.ValidationError("You have already replied on this reply")
        serializer.save(reply_id=reply_id)


class CommentOnReplyListView(ListAPIView):
    serializer_class = CommentOnReplySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        reply_id = self.kwargs["reply_id"]
        return CommentOnReply.objects.filter(reply_id=reply_id)


class HasAccessToComment(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        hosts_id = set(Property.objects.all().values_list("owner_id", flat=True))
        return user_id in hosts_id


class CommentOnUserCreateView(CreateAPIView):
    serializer_class = CommentOnUserSerializer
    permission_classes = [HasAccessToComment]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        reservation_id = self.kwargs["reservation_id"]
        reservation = get_object_or_404(Reservation, id=reservation_id, user_id=user_id)
        queryset = CommentOnUser.objects.filter(reservation=reservation).order_by("id")
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = get_object_or_404(User, pk=self.kwargs["user_id"])
        context.update({"user": user})
        return context

    def perform_create(self, serializer):
        user_id = self.kwargs["user_id"]
        reservation_id = self.kwargs["reservation_id"]
        user = self.request.user
        reservation = get_object_or_404(Reservation, id=reservation_id)
        if user != reservation.host:
            raise serializers.ValidationError(
                "You are not authorized to leave a comment for this user"
            )
        if reservation.user_id != user_id:
            raise serializers.ValidationError(
                "You are not authorized to leave a comment for this user"
            )
        if CommentOnUser.objects.filter(
            Q(reservation_id=reservation_id) & Q(reservation__user_id=user.id)
        ).exists():
            raise serializers.ValidationError(
                "You have already left a comment for this user"
            )
        serializer.save(user_id=user_id, reservation_id=reservation_id)


class CommentOnUserListView(ListAPIView):
    serializer_class = CommentOnUserSerializer
    permission_classes = [HasAccessToComment]
    pagination_class = CustomPagination

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        queryset = CommentOnUser.objects.filter(reservation__user_id=user_id).order_by(
            "id"
        )
        return queryset
