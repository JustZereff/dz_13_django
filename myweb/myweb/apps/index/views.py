from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegistrationForm, QuoteForm, AuthorForm, UserForm, UserProfileForm, CustomPasswordChangeForm
from django.views.generic.base import View
from .models import Author, Quote, Tag
import pprint

def index(request):
    quote_list = Quote.objects.order_by('author')
    return render(request, 'index/quote.html', {'quote_list': quote_list})
def authors(request):
    author_list = Author.objects.all()
    return render(request, 'authors/authors.html', {'author_list': author_list})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid username or password'})

    return render(request, 'registration/login.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            agree_to_rules = form.cleaned_data['agree_to_rules']
            # Проверка на уникальность имени пользователя
            if not User.objects.filter(username=username).exists():
                # Проверка на уникальность email пользователя
                if not User.objects.filter(email=email).exists():
                    # Создание пользователя, если имя уникально
                    user = User.objects.create_user(username=username, email=email, password=password)
                    # Логин пользователя
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    return redirect('index')
                else:
                    # Вывод ошибки, если email уже используется
                    return render(request, 'registration/register.html', {'form': form, 'error_message': 'Email already exists'})
            else:
                # Вывод ошибки, если имя пользователя уже используется
                return render(request, 'registration/register.html', {'form': form, 'error_message': 'Username already exists'})
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

class CustomLogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))
    
@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote_text = form.cleaned_data['quote']
            author = form.cleaned_data['author']
            tag_custom = form.cleaned_data['tag_custom']
            tags_input = tag_custom.split(',')
            tags_input = [tag.strip() for tag in tags_input if tag.strip()]
            # Создаем список объектов Tag для каждого тега
            tag_objects = [Tag.objects.get_or_create(tag=tag)[0] for tag in tags_input]
            new_quote = Quote.objects.create(quote=quote_text, author=author)
            # Привязываем теги к цитате
            new_quote.tag.add(*tag_objects)

            return redirect('index')
    else:
        form = QuoteForm()
    return render(request, 'index/add_quote.html', {'form': form})

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('authors')
    else:
        form = AuthorForm()
    return render(request, 'authors/add_author.html', {'form': form})

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'authors/author_detail.html', {'author': author})

@login_required
def user_settings(request):
    user = request.user
    user_form = UserForm(instance=user)
    profile = user.userprofile
    profile_form = UserProfileForm(instance=profile)
    password_form = CustomPasswordChangeForm(user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        password_form = CustomPasswordChangeForm(user, request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_settings')
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('user_settings')

    return render(request, 'user/user_settings.html', {'user_form': user_form, 'profile_form': profile_form, 'password_form': password_form})

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'user/password_reset.html'
    email_template_name = 'user/password_reset_email.html'
    html_email_template_name = 'user/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'user/password_reset_subject.txt'
