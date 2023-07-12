from django.urls import path

from .views import AuthorDetail, AuthorList, CategoryListView, PostList, PostDetail, PostCreate, PostDelete, PostEdit, PostSearch, subscribe

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('', PostList.as_view(), name='news'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view()),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit', PostEdit.as_view(), name='post_edit'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('post_create/', PostCreate.as_view(), name='post_create'),
    path('search/', PostSearch.as_view()),
    path('articles/create/', PostCreate.as_view(), name='post_create'),
    path('articles/<int:pk>/edit', PostEdit.as_view(), name='post_edit'),
    path('articles/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('author/', AuthorList.as_view(), name='authors'),
    path('author/<int:pk>/', AuthorDetail.as_view(), name='author'),
    #path('category/', CategoryList.as_view(), name='categories'),
    #path('category/<int:pk>/', CategoryList.as_view(), name='categories'),
    ##path('category/<int:pk>/', PostsOfCategoryList.as_view(), name='posts_of_category_list'),
    #path('category/<int:pk>/', PostsOfCategoryList.as_view(), name='category_list'),
    path('category/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('category/<int:pk>/', CategoryListView.as_view(), name='category_list2'),
    path('category/', CategoryListView.as_view(), name='category'),

    

]
