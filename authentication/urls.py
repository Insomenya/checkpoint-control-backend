from django.urls import path, include
from . import views

urlpatterns = [
    path('details', views.UserDetailsView.as_view(), name='user-details'),
    path('signup', views.UserSignupView.as_view(), name='user-signup'),
    path('setpass/<str:token>', views.SetPasswordView.as_view(), name='set-password'),
    path('users', views.UserListView.as_view(), name='user-list'),
    path('jwt/', include('djoser.urls.jwt')),
]