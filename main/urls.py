from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, LogoutView, TaskReorder, RegisterPage, CategoryCreate, CategoryUpdate, CategoryDelete

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task/create', TaskCreate.as_view(), name='task-create'),
    path('task/update/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('task/delete/<int:pk>', DeleteView.as_view(), name='task-delete'),
    path('task/reorder/', TaskReorder.as_view(), name='task-reorder'),

    path('category/add/', CategoryCreate.as_view(), name='category-add'),
    path('category/update/<int:pk>', CategoryUpdate.as_view(), name='category-update'),
    path('category/delete/<int:pk>', CategoryDelete.as_view(), name='category-delete')
]
