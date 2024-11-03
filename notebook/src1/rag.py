from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader,TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.messages import AIMessage,HumanMessage
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
import google.generativeai as Geminiai
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate,MessagesPlaceholder
import sqlite3,os,dotenv
from glob import glob

#------------------------------api-cONFIRGURATION---------------------------
dotenv.load_dotenv()
key = os.getenv('GOOGLE_API_KEY')
Geminiai.configure(api_key=key)
LLM = ChatGoogleGenerativeAI(model='gemini-1.5-flash',api_key=key,temperature=0.4)
google_embed = GoogleGenerativeAIEmbeddings(model='models/embedding-001',google_api_key=key)

#--------------------------------------ConversationalRAGChain--------------------
class ConversationalRAGChain:
    def __init__(self):
        self.output = None
        self.chat_history = []
    
    async def data_collection(self):
        pdf_file = glob(r'C:\Users\gupta\OneDrive\Desktop\Projects\conversational_rag\Data\*.pdf')
        collected_data = []
        for data in pdf_file:
            loader = PyPDFLoader(data)
            async for page in loader.alazy_load():
                collected_data.append(page)
        return collected_data

    def data_split(self,collected_data):
        splitter = RecursiveCharacterTextSplitter(chunk_size=700,chunk_overlap=200)
        split_data = splitter.split_documents(collected_data)
        return split_data
    
    def FAISS(self,data=None,add=False):
        if not os.path.exists('FAISSdb/faiss_index'):
            if data is not None:
               vector_store = FAISS.from_documents(documents=data,
                                                   embedding=google_embed)
               vector_store.save_local('FAISSdb/faiss_index')
        else:
            vector_store = FAISS.load_local('FAISSdb/faiss_index',
                                                    embeddings=google_embed,allow_dangerous_deserialization=True)
            if add == True:
                if data is not None:
                    vector_store = FAISS.add_documents(documents=data)
                    vector_store.save_local('FAISSdb/faiss_index')
                    vector_store = FAISS.load_local('FAISSdb/faiss_index',
                                                    embeddings=google_embed,allow_dangerous_deserialization=True)            
        return vector_store
    
    
    def Contextualize_rag(self,db):
        retriever = db.as_retriever()
        prompt = ChatPromptTemplate.from_messages([
            ('system','give a chat history and the lastest user question \n which might be reference context in the chat history. formulate a standalone question which can be understood. without the chat history. Do not Answer the question. just formulate it if needed and otherwise retrun as it is'),
            MessagesPlaceholder(variable_name='chat_history'),
            ('human',"{input}")
        ])
        history_aware = create_history_aware_retriever(llm=LLM,retriever=retriever,
                                                       prompt=prompt)
        
        return history_aware
    
    def final_chain(self,history,query,chat):
        
        qa_prompt = ChatPromptTemplate.from_messages([('system',
                                                       'you are a helpful AI assistant'),
                                                      MessagesPlaceholder('chat_history'),("human","Context: {context}\n\n{input}")])
        question_answer_chain = create_stuff_documents_chain(llm=LLM,prompt=qa_prompt)
        rag_chain = create_retrieval_chain(history, question_answer_chain)
        self.output = rag_chain.invoke({"input": query, "chat_history":chat})
        return self.output
        
    def get_chat_history(self):
        self.chat_history.extend([
            HumanMessage(content=self.output['input']),
            AIMessage(content=self.output['answer'])
        ])
        return self.chat_history
