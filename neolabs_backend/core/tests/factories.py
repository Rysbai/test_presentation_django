import factory
from django.contrib.auth.models import User
from django.db.models.signals import post_save


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'example_username{0}'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')
    email = factory.Sequence(lambda n: 'example{0}@email.com'.format(n))

    first_name = 'Example first name'
    last_name = 'Example last name'
    is_superuser = False
    is_staff = False
    is_active = True

    @staticmethod
    def create_superuser(**kwargs):
        return UserFactory(is_superuser=True, is_staff=True, **kwargs)
