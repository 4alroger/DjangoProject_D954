from django import forms
from django_filters import FilterSet, ModelChoiceFilter, DateFilter

from .models import Author, Category, Post


class PostFilter(FilterSet):
    date = DateFilter(field_name='time_in', lookup_expr='gt', widget=forms.DateInput(attrs={'type': 'date'}), label='Дата публикации')
    title = ModelChoiceFilter(field_name='category', queryset=Category.objects.all(), label='Категория', empty_label='Все категории',)
    author = ModelChoiceFilter(field_name='author', queryset=Author.objects.all(), label='Автор', empty_label='Все авторы')

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
            'time_in': ['gt'],
        }

