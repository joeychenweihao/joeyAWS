from django.urls import path
# from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import register_view,  set_password_view,  CustomLoginView, create_competition_view, check_competition_name, registration_result_view

urlpatterns = [

    path('', views.home, name='home'),  
    path('bulletin/', views.bulletin_board, name='bulletin-board'),  
    path('refresh-table/', views.refresh_table, name='refresh_table'),
    path('user-profile/', views.user_profile, name='user_profile'),  

    path('manage/', views.bulletin_manage, name='bulletin-manage'),
    path('detail/<int:id>', views.bulletin_detail, name='bulletin-detail'),
    path('delete_bulletin', views.bulletin_del, name='bulletin_del'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', register_view, name='register'),
    path('set-password/<str:token>/', set_password_view, name='set_password_view'),


    # Join Competition
    path('join-competition/', views.join_competition, name='join_competition'),
    path('check-competition-name/', check_competition_name, name='check_competition_name'),
    path('create-competition/', create_competition_view, name='create_competition'),
    path('registration-result/', registration_result_view, name='registration_result'),
    
    
   # Forum
    path('forum/', views.forum, name='forum'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    # Post-related URLs (without 'forum' prefix)
    path('api/post/new/', views.api_create_post, name='create_post'),
    path('api/post/<int:pk>/delete/', views.api_delete_post, name='delete_post'),
    path('api/post/<int:post_id>/like/', views.api_like_post, name='like_post'),

    # Admin pin post
    path('post/<int:post_id>/pin/', views.pin_post, name='pin_post'),

    # Comment-related URLs with 'api' prefix
    path('api/comment/new/', views.api_create_comment, name='create_comment'),
    path('api/comment/<int:comment_id>/like/', views.api_like_comment, name='like_comment'),
    path('api/comment/<int:comment_id>/delete/', views.api_delete_comment, name='delete_comment'),

    path('user-profile/', views.user_profile, name='user_profile'),  
    path('user-competition/', views.user_competition, name='user_competition'), 
    path('admin_fun/', views.admin_fun, name='admin_fun'),  
    path('user-posts', views.user_posts, name='user-posts'),  
    path('user-comments/', views.user_comments, name='user-comments'),  
    path('user-verify-page/', views.user_verify_page, name='user-verify-page'),  
    path('verify-email/', views.user_verify_edit, name='verify_email'),  

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
