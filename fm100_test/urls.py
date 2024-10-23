from django.urls import path
from . import views

urlpatterns = [
    path('fm100-test/', views.FM100TestView.as_view(), name='fm100_test'),
    path('fm100-test-complete/<int:score>/<str:time_taken>/', views.FM100TestCompleteView.as_view(), name='fm100_test_completed'),
]