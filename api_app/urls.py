from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import CurrentUserView, JobDetailView, JobListView

urlpatterns = [
    path('v1/auth/token/', obtain_auth_token, name='api-token-auth'),
    path('v1/auth/me/', CurrentUserView.as_view(), name='api-current-user'),
    path('v1/jobs/', JobListView.as_view(), name='api-job-list'),
    path('v1/jobs/<slug:slug>/', JobDetailView.as_view(), name='api-job-detail'),
]
