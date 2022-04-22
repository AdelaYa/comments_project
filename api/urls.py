from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('posts/add/', views.PostCreate.as_view()),
    path('posts/<int:post_id>/', views.PostDetail.as_view()),
    path('comments/<int:post_id>/', views.CommentList.as_view()),
    path('comments/<int:post_id>/add', views.CommentCreate.as_view()),
    path('comments/<int:post_id>/<int:comment_id>/children', views.CommentChildren.as_view()),
]


