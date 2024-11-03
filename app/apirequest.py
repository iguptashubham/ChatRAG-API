import requests

def upload_file(file):
    url = 'http://127.0.0.1:8000/upload_pdf'
    files = {'upload_document': (file.name, file.getvalue(), file.type)}
    response = requests.post(url, files=files)
    return response.json()

def get_file_name():
    url = 'http://127.0.0.1:8000/file_name'
    response = requests.get(url=url)
    return response.json()

def add_file_vectordb():
    url = 'http://127.0.0.1:8000/store_pdf_vectordb'
    response = requests.get(url=url)
    if response.status_code==200:
        return 'stored Successfully'
    else:
        return 'not stored'

def llmresponse(sessionid, query):
    url = 'http://127.0.0.1:8000/rag_chain'
    params = {'enter_query': query, 'session_': sessionid}
    response = requests.post(url=url, params=params)
    if response.status_code == 200:
        print('Successful')
        return response.json()
    else:
        print('Failed')
        return {'error': 'Failed to get response'}
