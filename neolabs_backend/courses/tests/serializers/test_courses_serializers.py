from unittest import TestCase

from courses.serializers import CategorySerializer, CourseSerializer
from courses.tests.base import AbstractModelSerializersTest
from courses.tests.factories import CategoryFactory, CourseFactory


class CategorySerializerTest(AbstractModelSerializersTest, TestCase):
    serializer_class = CategorySerializer
    factory = CategoryFactory


class CourseSerializerTest(AbstractModelSerializersTest, TestCase):
    serializer_class = CourseSerializer
    factory = CourseFactory
