import streamlit as st
from utils import sidebar
from chatretrival import chat_retrive
from apirequest import llmresponse
import uuid

st.set_page_config('Chat_with_llm', layout='wide')
st.title('Custom ChatRAG :blue[Gemini-Flash]')
user_input = st.chat_input('Enter your message here...')

sidebar()

#-------------------------------

with st.sidebar:
    id = st.text_input('Enter sessionID Here')
    create = st.button('Create new sessionid')
    if create:
        new_session_id = str(uuid.uuid4())
        st.success(f'New session ID: {new_session_id}')
        
# Ensure session_id is handled correctly
if id:
    session_id = id
    st.write(f"Session --> {id}")
elif create:
    session_id = new_session_id
    st.write(f"Session --> {new_session_id}")
    
chat_history = chat_retrive(session_id='14be3bcd-9b17-48e0-81f8-ef05f6e94f36')

for chat in chat_history['chat history']:
    if chat['role']=='human':
        with st.chat_message('human'):
            st.write(chat['content'])
    if chat['role']=='ai':
        with st.chat_message('assistant'):
            st.markdown(chat['content'],unsafe_allow_html=True)

if user_input:
    response = llmresponse(sessionid='14be3bcd-9b17-48e0-81f8-ef05f6e94f36', query=user_input)
    st.write(response['LLMResponse'],unsafe_allow_html=True)
