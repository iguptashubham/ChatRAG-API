from src.rag import ConversationalRAGChain
from src.chat_db import InteractionDB
import uuid
import asyncio

chatragchain = ConversationalRAGChain()
chatdb = InteractionDB()
    
async def data_collection_and_store():
    data = await chatragchain.data_collection()
    split_data = chatragchain.data_split(collected_data=data)
    return split_data
    
async def store_data():
    data = await chatragchain.data_collection()
    split_data = chatragchain.data_split(collected_data=data)
    chatragchain.FAISS(data=split_data)
    return 'Store data Successfully'

def retrive_vector():
    #vector store retrival
    vector_store = chatragchain.FAISS(add=False)
    return vector_store

def chat_rag(db,session_id,query):
    
    chat_history = chatdb.retrieve_chat(session_id=session_id) #retrival chat from sql database
    history = chatragchain.Contextualize_rag(db) #history
    
    output = chatragchain.final_chain(history=history,query=query,chat=chat_history)
    
    #index data into sql data base 
    chatdb.index_data(session_id=session_id, ai_response=output['answer'],user_input=output['input'], model='Gemini-flash')
    print(output)
    return output

def return_chat_history():
    return chatragchain.get_chat_history()
    
def sql_history(session):
    chat = chatdb.retrieve_chat(session_id=session)
    return chat