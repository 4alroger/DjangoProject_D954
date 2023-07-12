from django.db import models  # импорт моделей
from django.contrib.auth.models import User  # импорт шаблона User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):  # наследуемся от класса Model
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # имя автора в соответствии с шаблоном User
    rating = models.IntegerField(default=0)  # рейтинг автора

    def update_rating(self):  # метод обновления рейтинга автора
        p_rating = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum'] * 3  # рейтинг
        # статьи/новости
        c_rating = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']  # рейтинг комментария
        c_other_rating = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rating'))['rating__sum']  # рейтинг комментариев сторонних пользователей

        self.rating = p_rating + c_rating + c_other_rating  # суммарный рейтинг
        self.save()

    
class Category(models.Model):  # класс Категорий
    objects = None
    name = models.CharField(max_length=128, unique=True)  # максмиальная длина 128 знаков, уникальное поле
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.name.title()

class Post(models.Model):  # класс Post
    news = 'NE'
    article = 'AR'

    CATSELECT = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    objects = None
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Author
    time_in = models.DateTimeField(auto_now_add=True)  # автоматическое присвоение даты и времени создания
    title = models.CharField(max_length=255)  # длина заголовка
    choice_field = models.CharField(max_length=2, choices=CATSELECT)  # поле выбора категории новость/статья
    content = models.TextField()  # содержание статьи/новости
    rating = models.IntegerField(default=0)  # рейтинг статьи/новости
    category = models.ManyToManyField(Category, through='PostCategory', related_name='PostCategory')  # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory)

# , default='article'

    def preview(self):  # предварительный просмотр новости/статьи
        return self.content[0:124] + '...' if len(self.content) > 124 else self.content  # возвращает первые 124 знака содержимого новости/статьи

    def like(self):  # Метод "Like" - увеличивает рейтинг поста на единицу
        self.rating += 1
        self.save()

    def dislike(self):  # Метод "Dislike" - уменьшает рейтинг поста на единицу
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.title.title()}: {self.content[:20]}... (Автор: {self.author})'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])


class PostCategory(models.Model):  # Промежуточная модель для связи «многие ко многим»
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Post
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Category


class Comment(models.Model):
    objects = None
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор)
    time_in = models.DateTimeField(auto_now_add=True)  # дата и время создания комментария
    content = models.TextField()  # текст комментария
    rating = models.IntegerField(default=0)  # рейтинг комментария

    def like(self):  # Метод "Like" - увеличивает рейтинг комментария на единицу
        self.rating += 1
        self.save()

    def dislike(self):  # Метод "Dislike" - уменьшает рейтинг комментария на единицу
        self.rating -= 1
        self.save()
