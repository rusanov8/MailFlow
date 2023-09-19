from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Blog
from blog.services import get_cached_articles


# Create your views here.
class BlogListView(ListView):  # контроллер для отображения списка статей
    model = Blog

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['articles'] = get_cached_articles()

        return context_data


class BlogDetailView(DetailView):  # контроллер для отображения одной статьи
    model = Blog

    def get_object(self, queryset=None):   # устанавливаем счетчик кол-ва просмотров
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

