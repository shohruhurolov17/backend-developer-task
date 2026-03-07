from rest_framework.viewsets import ModelViewSet
from apps.posts.serializers import (
    PostCommentSerializer,
    PostCreateUpdateSerializer,
    PostSerializer,
    PostCategorySerializer
)
from rest_framework.generics import ListCreateAPIView
from apps.posts.models import Post, PostComment, PostCategory
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['posts'])
class PostCategoryViewSet(ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer


@extend_schema(tags=['posts'])
class PostViewSet(ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = PostSerializer
    queryset = Post.objects.select_related('category').prefetch_related('comments')

    def get_serializer_class(self):
        if self.action in ['partial_update', 'update', 'create']:
            return PostCreateUpdateSerializer
        return PostSerializer
    
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                PostSerializer(serializer.instance).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response({
            "error": str(serializer.errors)
        }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['posts'])
class PostCommentListCreateView(ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = PostCommentSerializer

    def get_post(self):

        try:
            return Post.objects.get(id=self.kwargs['post_id'])
        
        except Post.DoesNotExist:
            raise NotFound({
                "error": "Post not found"
            })
    
    def get_queryset(self):

        post = self.get_post()
        return PostComment.objects.filter(post=post)

    def create(self, request, post_id=None):

        post = self.get_post()

        serializer = self.get_serializer(data=request.data, context={
            'post': post
        })

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({
            "error": str(serializer.errors)
        }, status=status.HTTP_400_BAD_REQUEST)


        

