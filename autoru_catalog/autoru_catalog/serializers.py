from rest_framework.serializers import ModelSerializer

from autoru_catalog.models import Mark, Model


class MarkListSerializer(ModelSerializer):
    class Meta:
        model = Mark
        fields = '__all__'


class ModelsListSerializer(ModelSerializer):
    class Meta:
        model = Model
        fields = ('name',)


class UpdateAutoruCatalogSerializer(ModelSerializer):
    class Meta:
        model = Mark
        fields = '__all__'
