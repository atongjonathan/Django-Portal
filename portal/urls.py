from django.urls import path
from . import views
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("forgot", views.forgot, name="forgot"),
    path("recover", views.recover, name="recover")
    # path("test", views.test, name="test")
]