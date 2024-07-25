from blog.models import Page, Post
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView

PER_PAGE = 9

class PostListView(ListView):

    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering = '-pk', 
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published() # type: ignore


    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_published=True)
    #     return queryset


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context.update({
            'page_title': 'Home - ',
        })

        return context


# def index(request):

#     # Function Based Views -> Funções
#     # Class Bases Views -> Classes (POO)
#     # https://docs.djangoproject.com/en/5.0/ref/class-based-views/
    
#     posts = Post.objects.get_published() # type: ignore

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': 'Home - ',
#         }
#     )

def created_by(request, author_pk):
    
    user = User.objects.filter(pk=author_pk).first()

    if user is None:
        raise Http404()

    posts = (
        Post.objects.get_published() # type: ignore
        .filter(created_by__pk=author_pk)
    )

    user_full_name = user.username

    if user.first_name: # type: ignore
        user_full_name = f'{user.first_name} {user.last_name}' # type: ignore

    page_title = 'Posts de ' + user_full_name  + ' - '

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )

def category(request, slug):
    
    posts = (
        Post.objects.get_published() # type: ignore
        .filter(category__slug=slug)
    )

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()

    page_title = f'{page_obj[0].category.name} - Categoria - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )

def tag(request, slug):
    
    posts = (
        Post.objects.get_published() # type: ignore
        .filter(tags__slug=slug)
    )

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()
    
    page_title = f'{page_obj[0].tags.first().name} - Tag - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )

def search(request):
    
    search_value = request.GET.get('search', '').strip()

    posts = (
        Post.objects.get_published() # type: ignore
        .filter(
            # Título contém search_value OU
            # Excerto contém search_value OU
            # Conteúdo contém search_value
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
         )[:PER_PAGE]
    )
    
    page_title = f'{search_value[:30]} - Search - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
            'page_title': page_title,
        }
    )


def page(request, slug):

    page_obj = (
        Page.objects
        .filter(is_published=True)
        .filter(slug=slug)
        .first()
    )
    
    if page_obj is None:
        raise Http404()

    page_title = f'{page_obj.title} - Página - '

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_obj,
            'page_title': page_title,
        }
    )


def post(request, slug):

    post_obj = (
        Post.objects.get_published() # type: ignore
        .filter(slug=slug)
        .first()
    )

    if post_obj is None:
        raise Http404
    
    page_title = f'{post_obj.title} - Post - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'page_title': page_title,
        }
    )
