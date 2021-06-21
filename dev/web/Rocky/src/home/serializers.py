from annoying.functions import get_object_or_None
from django.db.models import Count
from django.conf import settings
from django.db import connection
from rest_framework import serializers







class NewDonationSerializer(serializers.Serializer):
	name 					=	serializers.CharField(max_length = 64)
	contact_number			=	serializers.CharField(max_length = 64, required = False)
	amount					=	serializers.IntegerField()
