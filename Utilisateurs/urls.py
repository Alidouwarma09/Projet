# Utilisateurs/urls.py
from django.urls import path
from .views import CustomLoginView, Index, Profile, CustomLogoutView, InscriptionView, CustomUserListView, \
    UserRegistrationView, message_list

app_name = 'utilisateurs'

urlpatterns = [
    path('', CustomLoginView.as_view(), name='connexion'),
    path('deconnexion/', CustomLogoutView.as_view(next_page='utilisateurs:connexion'), name='deconnexion'),
    path('inscription/', InscriptionView.as_view(), name='inscription'),
    path('index/', Index, name='Index'),
    path('index/', Index, name='Index'),
    path('profile/', Profile, name='Profile'),
    path('api/users/', CustomUserListView.as_view(), name='user-list'),
    path('api/inscription/', UserRegistrationView.as_view(), name='inscription_react'),
    path('api/messages/', message_list, name='message-list'),

]
