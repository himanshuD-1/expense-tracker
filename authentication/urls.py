from .views import CompletePasswordReset, EmailValidateView, LogOutView, LoginView, RegisterationView, ResetPasswordResetEmail, UsernameValidateView, VerificationView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', RegisterationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('validate-user/',csrf_exempt( UsernameValidateView.as_view()), name='validate-user'),
    path('validate-email/', csrf_exempt(EmailValidateView.as_view()), name='validate-email'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('set-new-password/<uidb64>/<token>', CompletePasswordReset.as_view(), name='reset-user-password'),
    path('reset-link', ResetPasswordResetEmail.as_view(), name='reset-password'),
]
