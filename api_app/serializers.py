from django.contrib.auth import get_user_model
from rest_framework import serializers

from admin_app.models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            'slug',
            'company_name',
            'job_title',
            'job_description',
            'location',
            'salary',
            'job_type',
            'employment_type',
        )


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username',)
