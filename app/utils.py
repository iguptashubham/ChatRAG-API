import streamlit as st
from apirequest import upload_file,get_file_name,add_file_vectordb
from chatretrival import chat_retrive

def sidebar():
    with st.sidebar:
        st.markdown('#### ChatRAG')
        with st.container(border=True):
            st.write('Upload Documents')
            #upload file
            file = st.file_uploader(label='upload File')
            if file is not None:
                response = upload_file(file=file)
                st.write('File uploaded Successfully')
                st.write(response)
                
            #return file name
            st.write('Get File Names')
            button = st.button(label='click to get file name')
            if button:
                filename = get_file_name()
                #for file in filename['file']:
                st.json(filename)
                
            st.write('Add Document in VectorStore')
            button_ = st.button('Add in FAISS')
            if button_:
                button=add_file_vectordb()
                st.spinner()
                st.write(button)
            