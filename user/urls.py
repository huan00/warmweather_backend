from django.urls import path, include

from .views import RegisterUser, LoginView, UpdateView, DeleteView, get_outfit, get_my_outfit

urlpatterns = [
    path('register', RegisterUser.as_view(), name='create_user'),
    path('login', LoginView.as_view(), name='login_user'),
    path('update/<int:pk>', UpdateView.as_view(), name='update_user'),
    path('delete/<int:pk>', DeleteView.as_view(), name='delete_user'),


    path('getmyoutfit', get_my_outfit, name='get_my_outfit'),
    path('getoutfit', get_outfit, name='get_outfit'),
]
