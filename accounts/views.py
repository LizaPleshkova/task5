from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import View
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import reverse, redirect
from .models import UserProfile
from rest_framework.viewsets import ModelViewSet
from .serializers import UserProfileSerializer
from rest_framework.decorators import api_view
from django.contrib import messages


class UsersListView(LoginRequiredMixin, View):
    def get(self, request):
        users = UserProfile.objects.all()
        return render(request, 'accounts/users_list.html', context={
            'users': users
        })


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {'form': login_form}
        return render(request, 'authorization/login.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if UserProfile.objects.get(user=user).status == 'Banned':
                    messages.error(request, 'Вы заблокированы!')
                    return redirect('login')
                login(request, user)
                return redirect('users_list')
        username = login_form.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            print('asd')
            messages.error(request, f'Пользователя с логином {username} не существует!')
        return redirect('login')


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {'form': register_form}
        return render(request, 'authorization/registration.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.username = register_form.cleaned_data['username']
            new_user.email = register_form.cleaned_data['email']
            new_user.save()
            new_user.set_password(register_form.cleaned_data['password'])
            new_user.save()
            UserProfile.objects.create(user=new_user, status='Unbanned')
            user = authenticate(username=register_form.cleaned_data['username'],
                                password=register_form.cleaned_data['password'])
            login(request, user)
            return redirect('users_list')

        context = {'form': register_form}
        return render(request, 'authorization/registration.html', context)


@api_view(['DELETE'])
def user_delete(request, pk):
    print(" popal")
    own_user_profile = UserProfile.objects.get(user=request.user)
    user_profile_to_delete = UserProfile.objects.get(id = pk)
    if user_profile_to_delete == own_user_profile:
        logout(request)
    user_profile_to_delete.delete()
    user_profile_to_delete.user.delete()
    return Response('Удалено')


class UserProfileApiView(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def update(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            instance = self.get_object()
            if instance.user.id == request.user.id and request.data['status'] == 'Banned':
                print(" from baned myself")
                logout(request)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response('Wrong!')
