from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from courses.models import Course
from courses.serializers import CourseSerializer


class CoursesListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny, ]

        else:
            permission_classes = [IsAuthenticated, IsAdminUser]

        return [permission() for permission in permission_classes]


class CourseRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny, ]

        else:
            permission_classes = [IsAuthenticated, IsAdminUser]

        return [permission() for permission in permission_classes]
