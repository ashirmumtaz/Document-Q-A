import os


from langchain_ollama.llms import OllamaLLM
from langchain.document_loaders import UnstructuredFileLoader
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import CharacterTextSplitter

from langchain.chains import RetrievalQA


working_dir = os.path.dirname(os.path.abspath(__file__))

llm = OllamaLLM(model= "gemma2:2b", temperature=0,)

embeddings= HuggingFaceBgeEmbeddings()

def get_answer(file_name, query):
    file_path = f"{working_dir}/{file_name}"
    ##Loading the document
    loader = UnstructuredFileLoader(file_path)
    documents = loader.load()

    ##create text chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200,separator='/n',)
    text_chunk = text_splitter.split_documents(documents)

    ##vector embeddings from text chunks

    knowledge_base = FAISS.from_documents(text_chunk,embeddings)

    ##Building chain
    qa_chain= RetrievalQA.from_chain_type(
        llm,
        retriever = knowledge_base.as_retriever()
    )

    response = qa_chain.invoke({"query":query})

    return response["result"]