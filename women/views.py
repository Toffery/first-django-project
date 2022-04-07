from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from django.core.paginator import Paginator

from .forms import *
from .models import *
from .utils import *


# menu = [{'title': "About", 'url_name': 'about'},
#         {'title': "Add Page", 'url_name': 'addpage'},
#         {'title': "Contact", 'url_name': 'contact'},
#         {'title': "Log In", 'url_name': 'login'}
# ]


# def index(request):
#     posts = Women.objects.all()
#     context = {'posts': posts,
#                'menu': menu,
#                'title': 'Main Menu',
#                'cat_selected': 0}
#     return render(request, 'women/index.html', context=context)

class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Main Page')
        context.update(c_def)
        return context

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')


def about(request):
    cats = Category.objects.annotate(Count('women'))
    context = {
        'menu': menu,
        'title': 'About',
        'cats': cats,
        'cat_selected': None
    }
    if not request.user.is_authenticated:
        user_menu = menu.copy()
        user_menu.pop(1)
        context['menu'] = user_menu

    return render(request, 'women/about.html', context=context)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True  # 403

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add new page")
        context.update(c_def)
        return context


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#     else:
#         form = AddPostForm()
#
#     return render(request, 'women/addpage.html', {'menu': menu, 'title': 'Add Post', 'form': form})


def contact(request):
    # return HttpResponse('Contact')
    cats = Category.objects.annotate(Count('women'))
    context = {
        'menu': menu,
        'title': 'About',
        'cats': cats,
        'cat_selected': None
    }
    if not request.user.is_authenticated:
        user_menu = menu.copy()
        user_menu.pop(1)
        context['menu'] = user_menu
    return render(request, 'women/contact.html', context=context)



# def login(request):
#     return HttpResponse('Log In')


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'women/post.html', context=context)


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        context.update(c_def)
        return context


# def show_category(request, cat_slug):
#     posts = Women.objects.filter(cat__slug=cat_slug)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {'posts': posts,
#                'menu': menu,
#                'title': cat_slug,
#                'cat_selected': cat_slug}
#     return render(request, 'women/index.html', context=context)


class ShowCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(
            cat__slug=self.kwargs['cat_slug'],
            is_published=True
        ).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(
            title='Категория - ' + c.name,
            cat_selected=c.pk
        )
        context.update(c_def)
        return context


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Registration')
        context.update(c_def)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    #form_class = AuthenticationForm
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Authentication")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def pageNotFound(request, exception):

    return HttpResponseNotFound('<h1>Вы кто такие? Я вас не звал. Идите нахуй!</h1>')
