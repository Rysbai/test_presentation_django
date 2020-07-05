from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from core.tests.factories import UserFactory
from courses.models import Course
from courses.tests.factories import CourseFactory, CategoryFactory


class CoursesAPITests(TestCase):
    default_request_headers = {
        "content_type": 'application/json'
    }

    def get_user_with_token(self, **user_kwargs):
        user = UserFactory(**user_kwargs)
        token, _ = Token.objects.get_or_create(user=user)

        return user, token

    def is_equal_courses_dict(self, first: dict, second: dict):
        self.assertEqual(first['name'], second['name'])

    def test_courses_list_should_return_all_courses(self):
        courses = CourseFactory.create_many()

        url = reverse('courses:courses_list_create')

        response = self.client.get(url, **self.default_request_headers)
        body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(body), len(courses))
        for i in range(len(courses)):
            self.is_equal_courses_dict(body[i], courses[i].__dict__)

    def test_create_course_should_return_unauthorized_if_token_is_incorrect(self):
        category = CategoryFactory()

        url = reverse('courses:courses_list_create')
        data = CourseFactory.get_json_data(category=category)

        response = self.client.post(url, data=data, **self.default_request_headers)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_course_should_return_forbidden_if_user_is_not_staff(self):
        category = CategoryFactory()
        user = UserFactory(is_superuser=False, is_staff=False)
        token, _ = Token.objects.get_or_create(user=user)

        url = reverse('courses:courses_list_create')
        data = CourseFactory.get_json_data(category=category)
        data['category'] = category.id
        headers = {
            "HTTP_AUTHORIZATION": f'Token {token}',
            **self.default_request_headers
        }

        response = self.client.post(url, data=data, **headers)
        body = response.json()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], 'You do not have permission to perform this action.')

    def test_create_course_should_return_created_course(self):
        category = CategoryFactory()
        user = UserFactory(is_staff=True)
        token, _ = Token.objects.get_or_create(user=user)

        url = reverse('courses:courses_list_create')
        data = CourseFactory.get_json_data(category=category)
        data['category'] = category.id
        headers = {
            "HTTP_AUTHORIZATION": f'Token {token}',
            **self.default_request_headers
        }

        response = self.client.post(url, data=data, **headers)
        body = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.is_equal_courses_dict(body, data)

    def test_retrieve_course_should_return_not_found_if_course_does_not_exist_with_given_pk(self):
        does_not_exist_pk = 1
        url = reverse('course:course_retrieve_update_delete', args=[does_not_exist_pk])

        response = self.client.get(url, **self.default_request_headers)
        body = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(body['detail'], 'Not found.')

    def test_retrieve_course_should_return_course_by_pk(self):
        course = CourseFactory()
        url = reverse('course:course_retrieve_update_delete', args=[course.id])

        response = self.client.get(url)
        body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.is_equal_courses_dict(body, course.__dict__)

    def test_update_course_should_return_unauthorized_if_credentials_is_not_correct(self):
        course = CourseFactory()
        url = reverse('course:course_retrieve_update_delete', args=[course.id])
        updating_data = CourseFactory.get_json_data()

        response = self.client.put(url, updating_data, **self.default_request_headers)
        body = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(body['detail'], 'Authentication credentials were not provided.')

    def test_update_course_should_return_forbidden_if_user_is_not_staff(self):
        user = UserFactory(is_superuser=False, is_staff=False)
        token, _ = Token.objects.get_or_create(user=user)

        category = CategoryFactory()
        course = CourseFactory()
        url = reverse('course:course_retrieve_update_delete', args=[course.id])
        updating_data = CourseFactory.get_json_data(category_id=category.id)

        headers = {
            "HTTP_AUTHORIZATION": f'Token {token}',
            **self.default_request_headers
        }

        response = self.client.put(url, data=updating_data, **headers)
        body = response.json()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(body['detail'], 'You do not have permission to perform this action.')

    def test_update_course_should_update_course(self):
        user = UserFactory(is_staff=True)
        token, _ = Token.objects.get_or_create(user=user)

        course = CourseFactory()
        url = reverse('course:course_retrieve_update_delete', args=[course.id])
        new_category = CategoryFactory()
        updating_data = CourseFactory.get_json_data(category_id=new_category.id)

        headers = {
            "HTTP_AUTHORIZATION": f'Token {token}',
            **self.default_request_headers
        }

        response = self.client.put(url, data=updating_data, **headers)
        body = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.is_equal_courses_dict(body, updating_data)
        self.assertEqual(body['category'], updating_data['category'])

    def test_delete_course_should_return_unauthorized_if_credentials_is_not_correct(self):
        course = CourseFactory()
        url = reverse('course:course_retrieve_update_delete', args=[course.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_course_should_return_forbidden_if_user_is_not_staff(self):
        _simple_user, token = self.get_user_with_token()

        course = CourseFactory()
        url = reverse('course:course_retrieve_update_delete', args=[course.id])
        headers = {
            "HTTP_AUTHORIZATION": f'Token {token}',
            **self.default_request_headers
        }
        response = self.client.delete(url, **headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_course_should_return_not_found_if_course_does_not_exist_with_given_pk(self):
        does_not_exist_pk = 12345678
        _admin_user, token = self.get_user_with_token(is_staff=True)

        url = reverse('course:course_retrieve_update_delete', args=[does_not_exist_pk])
        headers = {
            "HTTP_AUTHORIZATION": f'Token {token}',
            **self.default_request_headers
        }
        response = self.client.delete(url, **headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_course_should_return_no_content(self):
        course = CourseFactory()
        _admin_user, token = self.get_user_with_token(is_staff=True)

        url = reverse('course:course_retrieve_update_delete', args=[course.id])
        headers = {
            "HTTP_AUTHORIZATION": f'Token {token}',
            **self.default_request_headers
        }
        response = self.client.delete(url, **headers)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_course_should_delete_course(self):
        course = CourseFactory()
        _admin_user, token = self.get_user_with_token(is_staff=True)

        url = reverse('course:course_retrieve_update_delete', args=[course.id])
        headers = {
            "HTTP_AUTHORIZATION": f'Token {token}',
            **self.default_request_headers
        }
        _response = self.client.delete(url, **headers)

        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(id=course.id)
