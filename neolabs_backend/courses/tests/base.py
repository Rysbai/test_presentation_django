import pytest


class AbstractModelSerializersTest:
    serializer_class = None
    factory = None

    @pytest.mark.django_db
    def test_should_includes_all_fields(self):
        instance = self.factory()
        serializer = self.serializer_class(instance)

        self.check_fields(serializer.data)

    def check_fields(self, data: dict):
        fields = self.serializer_class.Meta.fields
        data_keys = data.keys()

        for field in fields:
            assert field in data_keys
