from django.urls import path
from . import views

urlpatterns = [
    # ... existing URL patterns ...
    path('eye-sight-test/', views.EyeSightTestView.as_view(), name='eye_sight_test'),
    path('eye-sight-test-complete/<int:score>/<str:visual_acuity>/', views.EyeSightTestCompleteView.as_view(), name='eye_sight_test_completed'),
]