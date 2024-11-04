from django.conf import settings

import tiktoken
from langchain_openai import ChatOpenAI


__author__ = 'Ricardo'
__version__ = '0.1'


class OpenAISingleton():

    __client = None

    @classmethod
    def __get_connection(self):
        """
        This method create our client
        """

        client = ChatOpenAI(api_key=settings.OPENAI_API_KEY,)

        return client

    def __new__(cls, *args, **kwargs):

        if cls.__client == None:

            # making connection
            cls.__client = cls.__get_connection()

        return cls.__client

    @classmethod
    def create_single_completion_message(cls, system_message: str, prompt: str):
        """
        This method create a new completion message to single tasks

        :param system_message: a string being the system message
        :param prompt: a string being the prompt
        :return: a completion message
        """

        from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

        response = cls.__client.invoke(
            [SystemMessage(content=system_message),
             HumanMessage(content=prompt)]
        )

        return response

    @classmethod
    def create_chat_completion_message(cls, history: list):
        """
        This method create a new completion message to chat tasks

        :param system_message: a string being the system message
        :param prompt: a 
        :return: a completion message
        """

        return cls.__client.invoke(history)
