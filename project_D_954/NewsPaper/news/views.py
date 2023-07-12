# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from datetime import datetime
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from NewsPaper import settings

from .filters import PostFilter
from .forms import PostForm
from .models import Author, Category, Post
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail


def send_notifications(preview, pk, title, subscribers):
    html_contect = render_to_string(
        'email_notification.html',
        {
            'content': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=['rusamph@yandex.ru'],    # тут пишем to=subscribe для отправки на почту подписчикам, для теста моя
    )
    # print(settings.DEFAULT_FROM_EMAIL)
    msg.attach_alternative(html_contect, 'text/html')
    msg.send()


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_in'] = datetime.utcnow()
        context['categories'] = Category.objects.all()
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной новости
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем пост
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = '-time_in'
    filterset_class = PostFilter
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    context_object_name = 'post_delete'
    success_url = reverse_lazy('posts_list')


class PostCreate(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'news.add_post'
    model = Post
    template_name = 'create.html'
    context_object_name = 'post_create'
    form_class = PostForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if 'news' in self.request.path:
            choice_field = 'NE'
        elif 'articles' in self.request.path:
            choice_field = 'AR'
        self.object.choice_field = choice_field
        return super().form_valid(form)


class PostEdit(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'edit.html'
    context_object_name = 'post_edit'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class AuthorList(ListView):
    model = Author
    ordering = '-user'
    template_name = 'authors.html'
    context_object_name = 'authors'
    paginate_by = 10


class AuthorDetail(DetailView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Author.objects.get(pk=self.kwargs['pk']).post_set.all().order_by('-id')
        return context


#class CategoryList(ListView):
#    model = Post
#    template_name = 'categories.html'
    #template_name = 'category_list.html'
#    context_object_name = 'categories'


#    def get_queryset(self):
#        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
#        queryset = Post.objects.filter(category=self.category).order_by('-time_in')
#        return queryset

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
#        context['category'] = self.category
#        return context

    
#class PostsOfCategoryList(ListView):
#    model = Post
#    ordering = '-id'
#    template_name = 'category_list.html'
#    #template_name = 'posts_of_cateory_list.html'
#    #posts.html'
#    context_object_name = 'posts'

#    def get_queryset(self):
#        self.queryset = Category.objects.get(pk=self.kwargs['pk']).PostCategory.all()
#        return super().get_queryset()


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list2.html'
    context_object_name = 'category_news_list'


    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-time_in')
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context







@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы подписались на категорию: '
    return render(request, 'subscribe.html', {'category': category, 'message': message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    message = 'Вы отписались от категории: '
    return render(request, 'subscribe.html', {'category': category, 'message': message})



def index(request):
    return HttpResponse("Привет. Вы на главной странице приложения NewsPaper!")
