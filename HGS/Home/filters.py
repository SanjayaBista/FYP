from pyexpat import model
import django_filters
from .models import *

class ProdFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['name']