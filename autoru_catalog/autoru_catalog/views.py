import requests
from bs4 import BeautifulSoup
from django.db.models.query import QuerySet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from autoru_catalog.models import Mark, Model
from autoru_catalog.serializers import MarkListSerializer, ModelsListSerializer, UpdateAutoruCatalogSerializer


def take_autoru_data() -> dict:
    """
    Получение данных всех марок и моделей из каталога авто.ру
    :return: словарь, в котором ключами являются марки, а значениями являются списки моделей
    """
    url_take = "https://auto-export.s3.yandex.net/auto/price-list/catalog/cars.xml"
    autoru_request = requests.get(url_take)
    autoru_content = BeautifulSoup(markup=autoru_request.content, features="xml")

    result = {}
    marks = autoru_content.find_all('mark')
    print(type(marks))
    for mark in marks:
        mark_name = mark['name']

        # используется set для отбора уникальных значений моделей
        models = {folder['name'].split(',')[0] for folder in mark.find_all('folder')}
        result[mark_name] = models
    return result


class MarksListView(ModelViewSet):
    serializer_class = MarkListSerializer
    queryset = Mark.objects.all()


class ModelsOfMarkListView(mixins.ListModelMixin,
                           GenericViewSet):
    serializer_class = ModelsListSerializer

    def get_queryset(self):
        mark = self.kwargs.get('mark_pk')  # получение pk марки, для поиска моделей этой марки
        queryset = Model.objects.filter(mark=mark)  # получение всех моделей требуемой марки
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset


class UpdateAutoruCatalogView(mixins.ListModelMixin,
                              GenericViewSet):
    queryset = Mark.objects.all()
    serializer_class = UpdateAutoruCatalogSerializer

    def list(self, request, *args, **kwargs):

        # удаление старых данных из БД
        Mark.objects.all().delete()

        # получение данных из каталога авто.ру
        autoru_data = take_autoru_data()

        # создание списков новых марок и моделей, которые будут добавлены в БД
        new_marks = []
        new_modelds = []

        for mark, models in autoru_data.items():
            new_mark = Mark(name=mark)
            new_marks.append(new_mark)  # добавление созданной марки в список
            for model in models:
                new_modeld = Model(name=model, mark=new_mark)
                new_modelds.append(new_modeld)  # добавление созданной модели в список

        # запись всех новых марок и моделей в БД общими запросами
        Mark.objects.bulk_create(new_marks)
        Model.objects.bulk_create(new_modelds)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
