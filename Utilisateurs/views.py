from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .forms import UserRegistrationForm, UserAuthenticationForm
from .models import CustomUser, Message
from .serializers import CustomUserSerializer, UserRegistrationSerializer, MessageSerializer


class InscriptionView(View):
    template_name = 'inscription.html'

    def get(self, request, *args, **kwargs):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('utilisateurs:connexion')
        else:
            print(form.errors)
            return render(request, self.template_name, {'form': form})


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.is_online = False
            request.user.last_logout = timezone.now()
            request.user.save()
        response = super().get(request, *args, **kwargs)
        return response


class CustomLoginView(LoginView):
    template_name = 'connexion.html'
    form_class = UserAuthenticationForm

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            user.is_online = True
            user.save()
            if user.role == 'admin':
                return reverse_lazy('admin:admin_dashboard')
            else:
                return reverse_lazy('utilisateurs:Index')
        return super().get_success_url()

    def form_invalid(self, form):
        print("erreur. Errors:", form.errors)
        return super().form_invalid(form)


@login_required(login_url='utilisateurs:connexion')
def Index(request):
    return render(request, 'index2.html')


@login_required(login_url='utilisateurs:connexion')
@user_passes_test(lambda u: u.role == 'user')
def Profile(request):
    utilisateurs = CustomUser.objects.exclude(role="admin").exclude(id=request.user.id)
    context = {'all_users': utilisateurs}
    return render(request, 'profile.html', context)


class CustomUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def message_list(request):
    if request.method == 'GET':
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
