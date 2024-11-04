import http
import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View

from recursos_humanos.documents.models import DocumentModel
from recursos_humanos.users.models import ConversationThreadModel, ConversationMessageModel, RoleEnum
from recursos_humanos.services.singleton.openai_singleton import OpenAISingleton
from recursos_humanos.services.singleton.pinecone_singleton import PineconeSingleton
from recursos_humanos.users.utils.conversation_manager import get_conversation_history


class ChatView(View):

    template_name = 'chatbot/chat.html'

    def get(self, request):

        return render(request, self.template_name)


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class SendMessageView(View):

    def post(self, request, *args, **kwargs):

        user_message = request.POST.get('user_message', '')
        conversation_thread = request.POST.get('conversation_thread', '')

        conversation_thread_gotten = ConversationThreadModel.objects.get(
            id=conversation_thread)

        if not all([user_message, conversation_thread]):
            return JsonResponse(
                {'error': 'Both user_message and conversation_thread are required.'},
                status=http.HTTPStatus.BAD_REQUEST
            )

        ConversationMessageModel.objects.create(
            conversation_thread=conversation_thread_gotten,
            role=RoleEnum.USER.value,
            message=user_message)

        response = OpenAISingleton.create_single_completion_message(
            system_message="Eres una inteligencia artificial avanzada que asocia preguntas de usuarios con el tema del documento que contenga la respuesta más probable, analizando el significado implícito de la pregunta y comparándolo con los títulos de cada documento. Indica solo el nombre del documento con información más relevante",
            prompt=f"""Instrucciones:
1. Analiza la pregunta del usuario y el significado general o el contexto que implica.
2. Revisa la lista de documentos con sus respectivos títulos y descripciones.
3. Selecciona el nombre del documento que más probablemente contenga la respuesta basándote en su título y descripción.

Por ejemplo, si la pregunta menciona una "fiesta," elige un documento titulado como "Eventos" o "Celebraciones" si está disponible, ya que el contexto de una fiesta puede relacionarse con estos temas.

pregunta: {user_message}
documentos existentes: {[{'title':document['title']} for document in DocumentModel.objects.filter(is_ready=True).values('title', 'description')]}\n\nResultado:""")

        response_content = response.content.strip("'\"")
        print(response_content)

        if not DocumentModel.objects.filter(title=response_content).exists():

            message = response_content
            ConversationMessageModel.objects.create(
                conversation_thread=conversation_thread_gotten,
                role=RoleEnum.ASSISTANT.value,
                message=response_content)

            history = get_conversation_history(conversation_thread_gotten)

            response = OpenAISingleton.create_chat_completion_message(history)
            message = response.content
            ConversationMessageModel.objects.create(
                conversation_thread=conversation_thread_gotten,
                role=RoleEnum.ASSISTANT.value,
                message=message)

        else:

            document = DocumentModel.objects.get(title=response_content)
            documents_gotten = PineconeSingleton.search_similarity_procedure(
                document=document, text=user_message)

            content = '\n----------------------\n'
            for i in documents_gotten:
                content += f'{i.page_content}\n\n'
            content += '----------------------\n'

            message = f"#### Información recuperada y actualizada del documento '{response_content}':\n{content}"
            print(message)

            ConversationMessageModel.objects.create(
                conversation_thread=conversation_thread_gotten,
                role=RoleEnum.ASSISTANT.value,
                message=message)

            history = get_conversation_history(conversation_thread_gotten)

            response = OpenAISingleton.create_chat_completion_message(history)
            message = response.content
            ConversationMessageModel.objects.create(
                conversation_thread=conversation_thread_gotten,
                role=RoleEnum.ASSISTANT.value,
                message=message)

        return JsonResponse({'msg': message}, status=http.HTTPStatus.OK)


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class SendVoiceMessageView(View):

    async def post(self, request, *args, **kwargs):
        user_message = request.POST.get('user_message', '')
        conversation_thread = request.POST.get('conversation_thread', '')

        response = await chatbot_repository.send_voice_message(thread_id, user_message)
        return JsonResponse(data=response['data'], status=response['status_code'])


@require_http_methods(["POST"])
def create_conversation_thread_view(request):
    """
    This view creates a conversation thread.
    """

    def get_years_since_created(instance):
        from datetime import date
        if instance.created_at:
            creation_date = instance.created_at.date()
            current_date = date.today()

            years_active = current_date.year - creation_date.year
            if (current_date.month, current_date.day) < (creation_date.month, creation_date.day):
                years_active -= 1
            return years_active
        return 0

    user = request.user

    conversation_thread = ConversationThreadModel.objects.create(
        user=user)
    ConversationMessageModel.objects.create(
        conversation_thread=conversation_thread,
        role=RoleEnum.SYSTEM.value,
        message=f"""Eres una inteligencia artificial avanzada de recursos humanos que responde dudas en base a documentos.

Debes de responder en base a la información de la persona de la que se te es dada y la información recuperada de documentos, que debes revisar de arriba a abajo.
Si una pregunta no se puede responder por que no se encuentra informacion suficiente de documentos tan solo dile que se comunique al correo nextwave@gmail.com, solo cuando no se encuentre información o cuando pregunte por el correo.

Esta es la información de la persona: Nombre:{user.first_name}, salary by month:{user.base_salary}, job title:{user.job_title}, department:{user.department}, años en la empresa:{get_years_since_created(user)}

#### Ejemplo
pregunta: ¿Habrá fiesta de recaudación de fondos?
información recuperada de documento: ...

*el documento menciona que habrá un evento de recaudación para beneficiarios, no es una fiesta, pero se asemeja*

los eventos, fiestas y celebraciones que obtengas de documentos debes mencionarlas, no importa por cual de las 3 se pregunte, debes mencionar todas las que obtengas.

resultado:si, habrá una fiesta que podemos llamar evento ...

debes tener esto en cuenta porque hay documentos que no hablan explicitamente sobre empleados, ya que hay algunos que tienen informacion como si fueran anuncios como de eventos y debes tratarlos como documentos.""")
    return JsonResponse({'conversation_thread': conversation_thread.id}, status=http.HTTPStatus.CREATED)


@require_http_methods(["POST"])
def delete_conversation_thread_view(request, conversation_thread):
    """
    This view deletes a conversation thread.
    """

    try:

        conversation_thread = ConversationThreadModel.objects.get(
            id=conversation_thread)
        conversation_thread.delete()

        return JsonResponse({}, status=http.HTTPStatus.NO_CONTENT)

    except ConversationThreadModel.DoesNotExist:
        return JsonResponse({'error': 'Conversation thread not found'}, status=http.HTTPStatus.NOT_FOUND)
