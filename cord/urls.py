from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('load_opinions/', views.load_opinions, name='load_opinions'),
    path('<int:post_pk>/post/', views.get_post, name='get_post'),
    path('profile/<str:username>', views.get_user_profile, name='get_user_profile'),
    path('<int:post_pk>/toggle_like/', views.toggle_like, name='toggle_like'),
    path('<int:post_pk>/toggle_sub_post_like/', views.toggle_sub_post_like, name='toggle_sub_post_like'),
    path('<int:post_pk>/toggle_sup_post_like/', views.toggle_sup_post_like, name='toggle_sup_post_like'),
    path('<str:target_user>/toggle_follow/', views.toggle_follow, name='toggle_follow'),
    path('<int:post_pk>/load_sub_post/', views.load_sub_post, name='load_sub_post'),
    path('share_opinion/', views.share_opinion, name='share_opinion'),
]