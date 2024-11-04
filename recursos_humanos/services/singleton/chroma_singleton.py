from uuid import uuid4

from django.conf import settings

from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import chromadb


__author__ = 'Ricardo'
__version__ = '0.1'


class ChromaSingleton():

    __client = None
    __vectorstore = None
    __embeddings = None

    @classmethod
    def __get_connection(cls, embedding_function):
        """
        This method create our client
        """

        client = chromadb.PersistentClient(path="chroma_db")

        if not 'recursos_humanos' in [coleccion.name for coleccion in client.list_collections()]:
            client.create_collection("recursos_humanos")

        return client

    def __new__(cls, *args, **kwargs):

        if cls.__client == None:

            # making connection
            cls.__embeddings = OpenAIEmbeddings(
                model=settings.EMBEDDING_MODEL,)
            cls.__client = cls.__get_connection(cls.__embeddings)
            cls.__vectorstore = Chroma(
                client=cls.__client, collection_name="recursos_humanos", embedding_function=cls.__embeddings)

        return cls.__client

    @classmethod
    def vectorize_file(cls, file, title):
        # Cargar el archivo PDF usando PyPDFLoader
        import os

        file_path = os.path.join(
            settings.MEDIA_ROOT, str(file))
        loader = PyPDFLoader(file_path)

        from langchain.text_splitter import RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=5000, chunk_overlap=900)

        chunked_documents = []

        for page_num, page in enumerate(loader.lazy_load(), start=1):
            chunks = text_splitter.split_text(page.page_content)

            for chunk in chunks:
                document = Document(
                    page_content=chunk,
                    metadata={"title": title,
                              "source": file.name, "page": page_num}
                )
                chunked_documents.append(document)

        cls.__vectorstore.add_documents(documents=chunked_documents)

    @classmethod
    def search_similarity_procedure(cls, text: str, document):
        """
        This method search the similarity in a text given

        :param text: an string beging our text to query
        :param document: the file we want to search in
        :return: a list with our documents 
        """

        return cls.__vectorstore.similarity_search(text, k=9, filter={'title': document.title})
