from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetConfirmView

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("forgot", views.forgot, name="forgot"),
    path("reset", views.recover, name="recover"),
    path("logout", views.logout_view, name="logout"),
    path("accounts/login/", views.login_view, name="login_redirect"),
    path("", views.choose, name="choose"),
    path("dashboard/<str:id>", views.dashboard, name="dashboard"),
    path("statement-print/<str:id>", views.statement_print, name="statement_print"),
    path("statement/<str:id>", views.statement, name="statement"),
    path("invite/<str:id>", views.invite, name="invite"),
    path("logged-out", views.logged_out, name="logged_out"),
    path("contact", views.contact, name="contact"),
    path("contact-us", views.contact_us, name="contact_us"),
    path("404", views.page_not_found, name="error_404"),
    path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),


    # path('forgot/<str:token>/', views.confirm_reset_password, name='confirm_reset_password'),
    # path("test", views.test, name="test")
]