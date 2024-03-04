from django.urls import path
from . import views


urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("forgot", views.forgot, name="forgot"),
    path("logout", views.logout_view, name="logout"),
    path("accounts/login/", views.login_view, name="login_redirect"),
    path("", views.choose, name="choose"),
    path("dashboard/<str:id>", views.dashboard, name="dashboard"),
    path("statement-print/<str:id>", views.statement_print, name="statement_print"),
    path("statement/<str:id>", views.statement, name="statement"),
    path("invite/<str:id>", views.invite, name="invite"),
    path("logged-out", views.logged_out, name="logged_out"),
    path("send-email", views.proceed, name="proceed"),
    path("contact", views.contact, name="contact"),
    path("contact-us", views.contact_us, name="contact_us"),
    path("404", views.page_not_found, name="error_404"),
    path("reset/<str:uidb64>/<str:token>/",
         views.set_password, name="set_password"),
    path('reset/<str:uidb64>/<str:token>/',
         views.reset, name='password_reset_confirm'),
    path('change/<str:uidb64>/<str:token>/',
         views.change, name='password_change_confirm'),
    path("modal/<id>", views.modal, name="modal"),
]
