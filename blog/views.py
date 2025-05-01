from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Tag
from game_features.models import Category


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
        context['tags'] = Tag.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/blog-detail.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related_posts = Post.objects.all().order_by('created_at')[:3]
        context['related_posts'] = related_posts
        return context
    
    

def create_blog(request):
    return render(request, 'blog/create-post.html')