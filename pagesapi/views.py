from .models import Contact
from .serializers import ContactSerializer
from rest_framework import viewsets

class ContactView(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer   
