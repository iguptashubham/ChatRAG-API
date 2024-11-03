from fastapi import FastAPI, HTTPException,UploadFile,Request
import os,shutil,uuid
from pydantic_models import QueryInput,LLMResponse
from utils import data_collection_and_store,store_data,retrive_vector,chat_rag,return_chat_history,sql_history

app = FastAPI(title='Custom ChatRAG Gemini Flash')

@app.post('/upload_pdf')
async def add_doc(upload_document:UploadFile):
    data_folder = r'C:\Users\gupta\OneDrive\Desktop\Projects\conversational_rag\Data'
    os.makedirs(data_folder,exist_ok=True)
    file_path = os.path.join(data_folder,upload_document.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_document.file, buffer)
    return {"filename": upload_document.filename, "location":file_path}

@app.get('/file_name')
async def get_filename():
    data_folder = r'C:\Users\gupta\OneDrive\Desktop\Projects\conversational_rag\Data'
    if not os.path.exists(data_folder):
        raise HTTPException(status_code=404, detail="Directory not found")
    
    try:
        files = os.listdir(data_folder)
        return {'file': files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/data_sample')
async def data_sample():
    data = await data_collection_and_store()
    #print(data)
    return {'data':data}
    
@app.get('/store_pdf_vectordb')
async def store(start: str = 'Y'):
    if start == 'Y':
        await store_data()
        return {'output': 'Task run successfully. Data Stores in Vector store'}
    else:
        return {'Task': 'Task Aborted'}
    
import uuid

@app.post('/rag_chain')
async def chat(enter_query: str, session_: str = None):
    if session_ is None:
        session_ = str(uuid.uuid4())
    vectorstore = retrive_vector()
    output = chat_rag(db=vectorstore, session_id=session_, query=enter_query)
    
    return {'LLMResponse': output['answer'],'session_id':session_}

@app.get('/recent_chat_history')
async def get_chat_history():
    chat_history = return_chat_history()
    return {'chat history':chat_history}

@app.get('/chat_history')
async def get_chat_history(session_id:str=None):
    if session_id is None:
        return {'output':'please enter Session_id'}
    else:
        chat_history = sql_history(session=session_id)
    return {'chat history':chat_history}