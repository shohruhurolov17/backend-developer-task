from django.urls import path, include
from apps.posts.views import (
    PostCategoryViewSet,
    PostViewSet,
    PostCommentListCreateView
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('categories', PostCategoryViewSet, basename='post_categories')
router.register('', PostViewSet, basename='posts')


urlpatterns = [
    path('posts/', include(router.urls)),
    path('posts/<int:post_id>/comments/', PostCommentListCreateView.as_view(), name='post_comment_list_create')
]
