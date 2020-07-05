from django.urls import path

from courses.views import CoursesListCreateAPIView, CourseRetrieveUpdateDeleteAPIView


app_name = 'course'

urlpatterns = [
    path('', CoursesListCreateAPIView.as_view(), name='courses_list_create'),
    path('<int:pk>', CourseRetrieveUpdateDeleteAPIView.as_view(), name='course_retrieve_update_delete')
]
