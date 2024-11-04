from uuid import uuid4

from django.conf import settings

from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings


__author__ = 'Ricardo'
__version__ = '0.1'


class PineconeSingleton():

    __client = None
    __index = None
    __vectorstore = None
    __embeddings = None

    @classmethod
    def __get_connection(cls):
        """
        This method create our client
        """

        cls.__embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,)

        from pinecone import Pinecone

        cls.__client = pc = Pinecone(
            api_key=settings.PINECONE_API_KEY)
        cls.__index = pc.Index('recursos-humanos')

        from langchain_pinecone import PineconeVectorStore

        cls.__vectorstore = PineconeVectorStore(
            index=cls.__index, embedding=cls.__embeddings)

    def __new__(cls, *args, **kwargs):

        if cls.__client == None:

            # making connection
            cls.__get_connection()

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
