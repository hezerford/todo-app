from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, FormView
from django.urls import reverse_lazy
from .models import Task, Category
from .forms import PositionForm

from django.db import transaction

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def get_default_category(user):
    category, created = Category.objects.get_or_create(name='Нет категории', user=None)
    category.user = user
    category.save()
    return category

class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):  
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'main/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or '' # запрашивается из поля
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input # после выполнения не оставляет поле пустым, а последним запросом

        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task # забирает модель из models
    context_object_name = 'task' 
    template_name = 'main/task.html' # желаемое имя шаблона

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'category', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        categories = Category.objects.filter(user=self.request.user)

        if categories.exists():
            default_category = None
            form.instance.category = default_category

        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'category', 'complete']
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))

class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'main/category_form.html'
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(user=self.request.user)
        context['form_title'] = 'Добавить категорию'
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name']
    template_name = 'main/category_update.html'
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(user=self.request.user)
        context['form_title'] = 'Изменить категорию'
        return context


class CategoryDelete(DeleteView, LoginRequiredMixin):
    model = Category
    context_object_name = 'category'
    success_url = reverse_lazy('tasks')

    def delete(self, request, *args, **kwargs):
        category = self.get_object()

        tasks_with_category = Task.objects.filter(category=category)
        general_category = Category.objects.get(user=None, name='Нет категории')
        tasks_with_category.update(category=general_category)

        return super().delete(request, *args, **kwargs)