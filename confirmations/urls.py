from django.urls import path
from .views import ConfirmationCreateView, ZoneConfirmationsView, CheckpointConfirmationsView

urlpatterns = [
    path('confirm', ConfirmationCreateView.as_view(), name='confirmation-create'),
    path('confirmed/zone/<int:zone_id>', ZoneConfirmationsView.as_view(), name='zone-confirmations'),
    path('confirmed/checkpoint/<int:checkpoint_id>', CheckpointConfirmationsView.as_view(), name='checkpoint-confirmations'),
] 