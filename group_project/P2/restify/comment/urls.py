from django.urls import path
from .views import (
    PropertyCommentCreateView,
    PropertyCommentListView,
    PropertyCommentReplyListView,
    PropertyCommentReplyView,
    CommentOnReplyCreateView,
    CommentOnUserCreateView,
    CommentOnReplyListView,
    CommentOnUserListView,
)

app_name = "comment"
urlpatterns = [
    path(
        "createcomment/<int:reservation_id>/<int:property_id>/",
        PropertyCommentCreateView.as_view(),
        name="createcomment",
    ),
    path(
        "commentonprop/<int:property_id>/",
        PropertyCommentListView.as_view(),
        name="listcomment",
    ),
    path(
        "commentonprop/<int:property_id>/<int:comment_id>/",
        PropertyCommentReplyListView.as_view(),
        name="listreply",
    ),
    path(
        "replycomment/<int:comment_id>/",
        PropertyCommentReplyView.as_view(),
        name="replycomment",
    ),
    path(
        "commentonreply/<int:reply_id>/",
        CommentOnReplyCreateView.as_view(),
        name="commentonreply",
    ),
    path(
        "commentonprop/<int:property_id>/<int:comment_id>/<int:reply_id>/",
        CommentOnReplyListView.as_view(),
        name="listreplyonreply",
    ),
    path(
        "commentonuser/<int:user_id>/<int:reservation_id>/",
        CommentOnUserCreateView.as_view(),
        name="createcommentonuser",
    ),
    path(
        "commentonuser/<int:user_id>/",
        CommentOnUserListView.as_view(),
        name="commentonuser",
    ),
]
