from django.db.models import QuerySet
from django_filters.rest_framework import CharFilter, DateFilter, Filter, FilterSet

from annalise_test.images.models import AnnaliseImage, ImageTag


class ImageTagsFilter(Filter):

    def filter(self, qs: QuerySet[AnnaliseImage], value: str) -> QuerySet[AnnaliseImage]:
        if not value:
            return qs

        values = value.split(",")
        for v in values:
            qs = qs.filter(tags=v)
        return qs


class AnnaliseImageFilter(FilterSet):
    tags = ImageTagsFilter()
    start_date = DateFilter(field_name="created_at__date", lookup_expr="gte")
    end_date = DateFilter(field_name="created_at__date", lookup_expr="lte")

    class Meta:
        model = AnnaliseImage
        fields = ("tags", "start_date", "end_date")


class TagFilter(FilterSet):
    name = CharFilter(lookup_expr="icontains")

    class Meta:
        model = ImageTag
        fields = ("name",)
