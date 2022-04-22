from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Post, Comment


class PostList(APIView):

    def get(self, request):
        posts = Post.objects.all()
        serializer_class = serializers.PostSerializer(posts, many=True)

        return Response({"posts": serializer_class.data})


class PostCreate(APIView):

    def post(self, request):
        serializer_class = serializers.PostSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            serializer_class.save()

            return Response({"new_post": serializer_class.data}, status=status.HTTP_201_CREATED)

        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):

    def get(self, request, post_id):
        post = Post.get_post_or_404(post_id=post_id)
        serializer_class = serializers.PostDetailSerializer(post)

        return Response({"post": serializer_class.data})


class CommentList(APIView):

    def get(self, request, post_id):
        post = Post.get_post_or_404(post_id=post_id)

        comments = Comment.objects.filter(post=post, level__lte=2)
        serializer_class = serializers.CommentSerializer(comments, many=True)

        return Response({"posts": serializer_class.data})


class CommentCreate(APIView):

    def post(self, request, post_id):
        post = Post.get_post_or_404(post_id=post_id)
        save_data = {
            "post": post.id,
            "content": request.data.get("content")
        }

        if request.data.get("parent_id"):
            parent = Comment.get_comment_or_404(request.data.get("parent_id"), post.id)
            save_data["parent"] = parent.id
            print(save_data)

        serializer_class = serializers.CommentSerializer(data=save_data)
        if serializer_class.is_valid(raise_exception=True):
            serializer_class.save()

            return Response({"new_comment": serializer_class.data}, status=status.HTTP_201_CREATED)

        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentChildren(APIView):

    def get(self, request, post_id, comment_id):
        comment = Comment.objects.get(post_id=post_id, id=comment_id)
        serializer_class = serializers.CommentSerializer(comment)

        if comment.level < 2:
            return Response({"comment": serializer_class.data, "children": []})

        serializer_children = serializers.CommentSerializer(comment.get_descendants(), many=True)

        return Response({"comment": serializer_class.data, "children": serializer_children.data})


