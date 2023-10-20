from django.urls import path, include

from .views import PromptView

urlpatterns = [ 
    path('prompt', PromptView.as_view(), name='prompt')
    
    ]

# urlpatterns += [
#     path('api-auth/', include('rest_framework.urls'))
# ]