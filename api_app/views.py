from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from admin_app.models import Job

from .serializers import CurrentUserSerializer, JobSerializer


class JobListView(generics.ListAPIView):
    queryset = Job.objects.order_by('-id')
    serializer_class = JobSerializer
    permission_classes = (AllowAny,)


class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'slug'


class CurrentUserView(APIView):
    def get(self, request):
        return Response(CurrentUserSerializer(request.user).data)
