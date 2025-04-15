from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GoodViewSet, ExpeditionCreateView, ExpeditionDetailView, 
    ExpeditionListView, CheckpointExpeditionsView, 
    CheckpointExpeditionsIdsView, ExpeditionStatusView
)

router = DefaultRouter()
router.register(r'goods', GoodViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('expedition', ExpeditionCreateView.as_view(), name='expedition-create'),
    path('expedition/<int:pk>', ExpeditionDetailView.as_view(), name='expedition-detail'),
    path('expeditions', ExpeditionListView.as_view(), name='expedition-list'),
    path('expeditions/<int:checkpoint_id>', CheckpointExpeditionsView.as_view(), name='checkpoint-expeditions'),
    path('expeditions/brief/<int:checkpoint_id>', CheckpointExpeditionsIdsView.as_view(), name='checkpoint-expeditions-ids'),
    path('expedition/status/<int:expedition_id>', ExpeditionStatusView.as_view(), name='expedition-status'),
] 