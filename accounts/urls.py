from django.urls import path, include
from django.contrib.auth import views as authViews
from . import views
from .forms import AuthenticationForm, UserPasswordChangeForm

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path(
        'login/',
        authViews.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=AuthenticationForm
            ),
        name='login'
    ),
    # path('login/', authViews.LoginView.as_view(), name='login'),
    path('logout/', authViews.LogoutView.as_view(), name='logout'),

    path('password_change/', authViews.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', authViews.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', authViews.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', authViews.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', authViews.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('email-verify/<str:key>/', views.email_verify, name='email_verify'),
    path(
        'change-password/',
        authViews.PasswordChangeView.as_view(
            template_name='account/change-password.html',
            success_url='/accounts/change-password-success',
            form_class=UserPasswordChangeForm
        ),
        name='change_password'
    ),
    path('change-password-success/', views.change_password_success, name='change_password_success'),

    path('profile/', views.profile_edit, name='profile'),
    path('ajax_upload_file', views.ajax_upload_file, name='account.ajax_upload_file'),
    path('ajax_user_update', views.ajax_user_update, name='account.ajax_user_update'),
    path('ajax_custom_banner_update', views.ajax_custom_banner_update, name='account.ajax_custom_banner_update'),
    path('ajax_user_change_liked_email', views.ajax_user_change_liked_email, name='account.ajax_user_change_liked_email'),

    path('check-mapillary-oauth', views.check_mapillary_oauth, name='check_mapillary_oauth'),
    path('check-mtpu-mapillary-oauth', views.MapillaryTokenRedirectView.as_view(), name='check_mtpu_mapillary_oauth'),
    path('check-mtpu-google-oauth', views.GoogleTokenRedirectView.as_view(), name='check_mtpu_google_oauth'),
    path('', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path('close/', views.account_close, name='account.account_close'),

    path('check_unconfirmed_user/', views.check_unconfirmed_user, name='check_unconfirmed_user'),
    path('retry_verify_user/<str:email>/', views.retry_verify_user, name='retry_verify_user')
]
