import datetime
import factory
from django.db.models.signals import post_save

from core.utils import is_json_serializable
from courses.models import Category, Course


@factory.django.mute_signals(post_save)
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: 'test_name{0}'.format(n))


@factory.django.mute_signals(post_save)
class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    category = factory.SubFactory('courses.tests.factories.CategoryFactory', )
    name = factory.Sequence(lambda n: 'test_name{0}'.format(n))
    start_date = datetime.datetime.now().date()

    @staticmethod
    def create_many(count=4, **kwargs):
        courses = []
        for _ in range(count):
            courses.append(
                CourseFactory(**kwargs)
            )

        return courses

    @staticmethod
    def get_json_data(**kwargs):
        course = CourseFactory.build(**kwargs)

        data = {}
        for key, value in course.__dict__.items():
            if is_json_serializable(value):
                data[key] = value

        data['start_date'] = course.start_date.strftime('%Y-%m-%d')
        data['category'] = course.category_id

        return data
