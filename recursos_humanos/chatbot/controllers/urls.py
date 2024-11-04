from django.urls import path

from ..views import chatbot_views


app_name = 'chatbot_app'


urlpatterns = [
    path('chat/', chatbot_views.ChatView.as_view(), name="chat"),
    path('chat/text-message/',
         chatbot_views.SendMessageView.as_view(), name="send_message"),
    path('chat/voice-message/', chatbot_views.SendVoiceMessageView.as_view(),
         name="send_voice_message"),
    path('create_conversation_thread/', chatbot_views.create_conversation_thread_view,
         name="create_conversation_thread"),
    path('delete_conversation_thread/<str:conversation_thread>/', chatbot_views.delete_conversation_thread_view,
         name="delete_conversation_thread"),
]
