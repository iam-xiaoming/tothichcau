from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Tag
from game_features.models import Category
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm
from django.contrib import messages
import logging
from django.urls import reverse
from users.models import MyUser

logger = logging.getLogger(__name__)


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all().order_by('-frequency')[:10]
        return context
    

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        user = get_object_or_404(MyUser, pk=pk)
        return Post.objects.filter(user=user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all().order_by('-frequency')[:10]
        return context

class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10
    
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        
        print(slug)
        
        category = get_object_or_404(Category, slug=slug)
        return Post.objects.filter(category=category).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all().order_by('-frequency')[:10]
        return context
    
    
    
class TagPostListView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10
    
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        
        print(slug)
        
        tag = get_object_or_404(Tag, slug=slug)
        return Post.objects.filter(tags__in=[tag]).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all().order_by('-frequency')[:10]
        return context    
    

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/blog-detail.html'
    
    
    def get_context_data(self, **kwargs):
        
        obj = self.get_object()
        obj.count_view += 1
        obj.save()
        
        context = super().get_context_data(**kwargs)
        related_posts = Post.objects.all().order_by('created_at')[:3]
        context['tags'] = Tag.objects.all().order_by('-frequency')[:10]
        context['related_posts'] = related_posts
        return context

    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create-post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        
        self.object = post

        tag_str = form.cleaned_data.get('tags', '')
        tag_list = [t.strip().lstrip('#') for t in tag_str.split(' ') if t.strip()]
        tag_objects = []
        for tag_name in tag_list:
            if len(tag_name) < 3:
                messages.error(self.request, f"Tag '{tag_name}' too short.")
                return self.form_invalid(form)
            tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
            tag_obj.frequency += 1
            tag_obj.save()
            tag_objects.append(tag_obj)

        post.tags.set(tag_objects)

        messages.success(self.request, "Post created successfully!")
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

