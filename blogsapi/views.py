from django.shortcuts import render
from .models import Blogs
from .serializers import BlogsSerializer
from rest_framework import viewsets
import base64
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


# class BlogsView(viewsets.ModelViewSet):
#     queryset = Blogs.objects.all()
#     serializer_class = BlogsSerializer

class BlogsView(viewsets.ModelViewSet):
    queryset = Blogs.objects.all()
    serializer_class = BlogsSerializer

#################### Limit parameter #################
    def get_queryset(self):
        queryset = Blogs.objects.all()
        limit = self.request.query_params.get("limit")

        if limit is not None:
            return queryset.order_by('-id')[:int(limit)]

        return queryset
###### convert video  in base 64 #####
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        # Check if 'image' is in the request data
        if 'video' in request.data:
            # Get the uploaded file
            uploaded_file = request.data['video']


            # Convert the file to base64
            try:
                base64_encoded = base64.b64encode(uploaded_file.read()).decode('utf-8')
            except Exception as e:
                return Response({'error': 'Error encoding file to base64.'}, status=status.HTTP_400_BAD_REQUEST)


            # Update the serializer's data to store the base64 encoded document
            serializer.validated_data['video_base64'] = base64_encoded


        serializer.save()  # Save the data to the database
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)