from rest_framework import serializers
from apps.posts.models import Post, PostComment, PostCategory


class PostCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PostCategory
        fields = (
            'id',
            'name'
        )


class PostCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostComment
        fields = (
            "id",
            "post",
            "text"
        )
        read_only_fields = (
            "id",
            "post"
        )


    def create(self, validated_data):

        validated_data['post'] = self.context['post']

        return PostComment.objects.create(**validated_data)


class PostSerializer(serializers.ModelSerializer):

    comments = PostCommentSerializer(many=True, read_only=True)

    category = PostCategorySerializer()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "body",
            "category",
            "comments"
        )
        read_only_fields = (
            "id",
            "comments"
        )

class PostCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            "title",
            "body",
            "category",
        )