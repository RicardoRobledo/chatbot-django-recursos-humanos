from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

from ..models import ConversationMessageModel, RoleEnum


__author__ = 'Ricardo'
__version__ = '0.1'


def get_conversation_history(conversation_thread):
    """
    This method gets a conversation history from a conversation thread.

    :param conversation_thread: the conversation thread
    :return: a formatted conversation history
    """

    history = []

    for conversation_message in ConversationMessageModel.objects.filter(conversation_thread=conversation_thread):

        if conversation_message.role == RoleEnum.SYSTEM.value:
            history.append(SystemMessage(content=conversation_message.message))
        elif conversation_message.role == RoleEnum.USER.value:
            history.append(HumanMessage(content=conversation_message.message))
        elif conversation_message.role == RoleEnum.ASSISTANT.value:
            history.append(AIMessage(content=conversation_message.message))
    
    return history
