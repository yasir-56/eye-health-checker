from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    path('color-blindness-test/', views.ColorBlindnessTestView.as_view(), name='color_blindness_test'),
    path('color-blindness-test-completed/', views.TestCompletedView.as_view(), name='color_blindness_test_completed'),

]
