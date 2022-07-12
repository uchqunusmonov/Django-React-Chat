from django.urls import path, include
from .views import (
    LoginView,
    CustomUserRegistrationView,
    UserProfileView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register("profile", UserProfileView)


urlpatterns = [
    path('', include(router.urls)),
    path('login', LoginView.as_view(), name="login"),
    path('register', CustomUserRegistrationView.as_view(), name="register"),
]