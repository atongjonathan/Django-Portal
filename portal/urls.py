from django.urls import path
from . import views
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("forgot", views.forgot, name="forgot"),
    path("recover", views.recover, name="recover"),
    path("logout", views.logout_view, name="logout"),
    path("accounts/login/", views.login_view, name="login_redirect"),
    # path('forgot/<str:token>/', views.confirm_reset_password, name='confirm_reset_password'),
    # path("test", views.test, name="test")
]