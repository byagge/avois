    # apps/posts/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm
from apps.notifications.models import Notification
from .models import Post
from apps.dynamic_content.utils import get_dynamic_message, weather
from apps.comments.models import Comment
from apps.likes.models import Like
from apps.tags.models import Tag
import logging
from django.db.models import Q
from apps.users.models import User

logging.basicConfig(level=logging.DEBUG)

# def homepage(request):
#     posts = Post.objects.all()
#     return render(request, 'index.html', {'posts': posts})

def homepage(request):
    # Получаем динамическое сообщение и теги
    dynamic_message = get_dynamic_message()
    tags = Tag.objects.all()

    # Проверяем наличие параметра для поиска и выбранного тега
    search_query = request.GET.get('query', '')
    selected_tag = request.GET.get('tag')
    
    # Начальное значение для постов
    posts = Post.objects.all()

    if selected_tag:
        # Фильтруем посты по тегу, если он выбран
        posts = posts.filter(tags__name=selected_tag)

    if search_query:
        # Фильтруем посты по ключевому слову в заголовке или содержимом, если есть поисковый запрос
        posts = posts.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )

    temperature = round(weather())  # Получаем только температуру

    context = {
        "dynamic_message": dynamic_message,
        "temperature": temperature,
        "recommended_posts": posts,  # Отфильтрованные посты
        "tags": tags,
        "selected_tag": selected_tag,
        "search_query": search_query,  # Чтобы отобразить текущий запрос в поле ввода
    }
    return render(request, 'index.html', context)


def weather_view(request):
    temperature = weather()  # Получаем только температуру
    print(f"Температура: {temperature}")  # Для отладки
    context = {
        "temperature": temperature
    }
    return render(request, 'parts/header.html', context)

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        # Создаем уведомление для автора поста
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                message=f'{request.user.username} liked your post',
                type='like'
            )
    return redirect('post_detail', pk=pk)

def retrieve(request, pk):
    # Получаем пост и связанные с ним комментарии
    post = get_object_or_404(Post, id=pk)
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    # Обработка добавления комментария
    if request.method == 'POST':
        if 'comment_text' in request.POST:  # Проверяем имя поля
            if request.user.is_authenticated:
                text = request.POST.get('comment_text')  # Получаем текст комментария
                if text:
                    Comment.objects.create(user=request.user, post=post, text=text)
                    messages.success(request, "Комментарий добавлен!")
                    return redirect('retrieve', pk=post.id)
                else:
                    messages.error(request, "Комментарий не может быть пустым.")
            else:
                return redirect('login')

        elif 'like' in request.POST:
            if request.user.is_authenticated:
                existing_like = Like.objects.filter(user=request.user, post=post).first()
                if existing_like:
                    existing_like.delete()
                    messages.info(request, "Лайк удален.")
                else:
                    Like.objects.create(user=request.user, post=post)
                    messages.success(request, "Лайк добавлен!")
            else:
                return redirect('login') 
            return redirect('retrieve', pk=post.id)

    likes_count = Like.objects.filter(post=post).count()

    # Замена для отображения изображения в контенте поста
    content_with_images = post.content.replace(
        '<!-- IMAGE -->', 
        f'<img src="{post.cover_image.url}" alt="Image" style="max-width: 100%; height: auto; margin: 30px 0px; display: grid; place-items: center;">'
    )

    # Температура из внешней функции
    temperature = round(weather())

    # Рекомендованные посты и теги
    recommended_posts = Post.objects.all()
    tags = post.tags.all()  # если у вас есть поле ManyToMany для тегов
    selected_tag = request.GET.get('tag')

    if selected_tag:
        posts = Post.objects.filter(tags__name=selected_tag)
    else:
        posts = Post.objects.all()

    # Автор поста
    author = post.author

    return render(request, 'retrieve.html', {
        'post': post,
        'comments': comments,
        'likes_count': likes_count,
        'content_with_images': content_with_images,
        'recommended_posts': recommended_posts,
        'tags': tags,
        "temperature": temperature,
        'author': author,
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()  # сохраняем пост и получаем его ID
            post.tags.set(request.POST.getlist('tags'))  # устанавливаем теги
            return redirect('retrieve', pk=post.id)  # перенаправляем, используя pk

    tags = Tag.objects.all()
    return render(request, 'create_post.html', {'tags': tags})

def my_posts(request):
    dynamic_message = get_dynamic_message()

    temperature = round(weather())
    posts = Post.objects.filter(author=request.user)
    return render(request, 'myposts.html', {'posts': posts, 'temperature': temperature, 'dynamic_message': dynamic_message})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    tags = Tag.objects.all()  # Получаем все теги для выбора
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            post.tags.set(request.POST.getlist('tags'))  # Устанавливаем выбранные теги
            return redirect('myposts')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post, 'tags': tags})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('myposts')
    return render(request, 'confirm_delete.html', {'post': post})