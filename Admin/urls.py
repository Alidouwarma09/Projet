# admin/urls.py
from django.urls import path
from .views import admin_dashboard, admin_create_user, admin_edit_user, admin_delete_user, tous_les_user, utilisateur, \
    Messages, Create, blog_list, BlogPostDetailView, share_post, All_Blog, delete_post, edit_post, view_blog, \
    active_utilisateur, desactive_utilisateur, Info_du_site, modifier_parametres

app_name = 'admin'
urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('create/', admin_create_user, name='admin_create_user'),
    path('edit/<int:user_id>/', admin_edit_user, name='admin_edit_user'),
    path('delete/<int:user_id>/', admin_delete_user, name='admin_delete_user'),
    path('user/', tous_les_user, name='tous_les_user'),
    path('utilisateur/', utilisateur, name='utilisateur'),
    path('messages/<int:user_id>/', Messages, name='messages'),
    path('create_blog/', Create, name='create'),
    path('list/', blog_list, name='post'),
    path('All_Blog/', All_Blog, name='All_Blog'),
    path('<int:blog_id>/', BlogPostDetailView.as_view(), name='blog_detail'),
    path('<int:blog_id>/share/', share_post, name='share_post'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('edit_post/<int:post_id>/', edit_post, name='edit_post'),
    path('view_blog/<int:post_id>/', view_blog, name='view_blog'),
    path('Active_utilisateur/<int:utilisateur_id>/', active_utilisateur, name='active_utilisateur'),
    path('Desactive_utilisateur/<int:utilisateur_id>/', desactive_utilisateur, name='desactive_utilisateur'),
    path('info_du_site/', Info_du_site, name='info_du_site'),
    path('modifier_parametres/<int:pk>/', modifier_parametres, name='modifier_parametres'),
]
