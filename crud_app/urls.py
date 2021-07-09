from django.urls import path, include

from crud_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/<int:post_id>', views.get_post, name='get_post'),
    path('posts/<int:post_id>/delete', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/update', views.update_post, name='update_post'),
    path('posts/add', views.add_post, name='add_post'),
    path('user/register', views.register, name='register'),

    path('user/', include('django.contrib.auth.urls')),
]