from django.urls import path

from .views import RegisterUser, LoginView, UpdateView, DeleteView, get_outfit, get_my_outfit, test_prompt

urlpatterns = [
    path('register', RegisterUser.as_view(), name='create_user'),
    path('login', LoginView.as_view(), name='login_user'),
    path('update/<int:pk>', UpdateView.as_view(), name='update_user'),
    path('delete/<int:pk>', DeleteView.as_view(), name='delete_user'),
    path('getoutfit', get_outfit, name='get_outfit'),
    path('getmyoutfit', get_my_outfit, name='get_my_outfit'),
    path('testprompt', test_prompt, name='test prompt')
]
