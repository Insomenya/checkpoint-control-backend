from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CheckpointViewSet

router = DefaultRouter()
router.register(r'checkpoints', CheckpointViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 