from django.urls import path
from accounts.forms import UserLoginForm, PwdResetForm
from accounts.views import SignUpView, PwdResetConfirmView, AccountDetailsView, AccountUpdateView
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordResetView,  
    PasswordResetCompleteView, 
    PasswordResetDoneView,
    
)

app_name = 'accounts'

urlpatterns = [
    path('login', LoginView.as_view(template_name='accounts/login.html', form_class=UserLoginForm, redirect_authenticated_user=True), name='login'),
    path('logout', LogoutView.as_view(next_page="accounts:login"), name='logout'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('<username>/<pk>', AccountDetailsView.as_view(), name='user_details'),
    path('update/<username>/<pk>', AccountUpdateView.as_view(), name='account_update'),
    path(
        'reset_password', 
        PasswordResetView.as_view(
            template_name='accounts/password/pwd__reset_form.html',
            form_class=PwdResetForm, 
            success_url='pwd_reset_email_sent/',
            email_template_name="accounts/password/pwd__reset_email.html"
            ), 

        name='password_reset'),

    path(
        'pwd_reset_email_sent',
        PasswordResetDoneView.as_view(
            template_name='accounts/password/pwd__reset_done.html'
        ),
        name='pwd_email_sent_confirm'
    ),
    
    path(
        'pwd_reset_complete',
        PasswordResetCompleteView.as_view(
            template_name='accounts/password/pwd__reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    path(
        'password/<uidb64>/<token>',
        PwdResetConfirmView.as_view(),
        name='pwd_reset_confirm'
    ),

    
]
