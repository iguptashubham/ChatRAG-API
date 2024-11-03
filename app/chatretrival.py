import requests

def chat_retrive(session_id):
    url = 'http://127.0.0.1:8000/chat_history'
    params = {'session_id':session_id}
    response = requests.get(url=url,params=params)
    if response.status_code ==200:
        return response.json()
    else:
        return {'unable to retrieve chats'}