from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'api/users', UserProfileApiView)

urlpatterns = [
    path('', UsersListView.as_view(), name='users_list'),
    path('users/delete/<int:pk>/', user_delete, name='delete'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='users_list'), name='logout'),
    path('registrations/', RegisterView.as_view(), name='register'),
]

urlpatterns += router.urls
