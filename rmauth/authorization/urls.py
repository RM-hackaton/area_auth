from django.urls import path

from .views import (
    RegistrationAPIView, LoginAPIView, CustomUserRetrieveUpdateAPIView, RefreshView, ProfileAPIView, ProfileIDAPIView,
    RequisitesAPIView, RequisitesIDAPIView, CreateRequisitesAPIView, CreateProfileAPIView
)


app_name = 'authorization'
urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user/', CustomUserRetrieveUpdateAPIView.as_view()),
    path('refresh/', RefreshView.as_view()),
    path('profile/', ProfileAPIView().as_view()),
    path('profile/<int:user_id>/', ProfileIDAPIView.as_view()),
    path('createprofile/', CreateProfileAPIView.as_view()),
    path('requisites/', RequisitesAPIView.as_view()),
    path('requisites/<int:user_id>/', RequisitesIDAPIView.as_view()),
    path('createrequisites/', CreateRequisitesAPIView.as_view())
]
