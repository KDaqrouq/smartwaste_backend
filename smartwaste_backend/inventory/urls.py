from django.urls import path
from .views import YourOwnAPIView

urlpatterns = [
    path('protected/', YourOwnAPIView.as_view()),
]