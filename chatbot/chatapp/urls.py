from django.urls import path
from .views import LoginAPI,SignupAPI,user_list,save_chat_history,get_chat_history

urlpatterns = [
  
    path('api/login/', LoginAPI.as_view(), name='login_api'),
    path('api/signup/', SignupAPI.as_view(), name='signup_api'),
    path('api/users/', user_list, name='user_list_api'),


    path('api/save-chat-history/', save_chat_history, name='save-chat-history'),
    path('api/get-chat-history/', get_chat_history, name='get-chat-history'),

]   
