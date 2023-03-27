from django.urls import path
from . import views
from apps.base.views import PasswordResetView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Add other views and URLs here as needed
]
