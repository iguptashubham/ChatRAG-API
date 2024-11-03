# ChatRAG API
Welcome to the Custom Trained Gemini Flash (CTGF) project! This project aims to create a sophisticated conversational AI application that integrates the Gemini Flash large language model using FastAPI and Streamlit.

# Workflow
![ChatRAG-API](https://raw.githubusercontent.com/iguptashubham/ChatRAG-API/refs/heads/main/workflow/chatrag-workflow.png)

## Project Overview

Custom Trained Gemini Flash (CTGF) helps in Chat with your custom data, providing a seamless, interactive user experience for querying and retrieving data, leveraging advanced AI capabilities for contextual and engaging conversations.

## Key Components

### FastAPI Backend
- **Endpoints**: Handles file uploads, data retrieval, and conversational queries.
- **Data Management**: Manages data storage and vector databases using FAISS.
- **Asynchronous Processing**: Efficiently manages asynchronous tasks to provide real-time responses.

### Streamlit Frontend
- **User Interface**: A dynamic and user-friendly interface for uploading files, initiating chat sessions, and viewing conversation history.
- **Real-time Interactivity**: Enables users to interact with the AI in real-time, providing instant feedback and response.

### Gemini Flash Model Integration
- **Conversational AI**: Utilizes the advanced capabilities of the Gemini Flash model to generate context-aware, relevant responses.
- **RAG Chain**: Implements a Retrieval-Augmented Generation (RAG) chain to enhance the AI's ability to retrieve accurate information and generate meaningful responses based on user queries.

## Features
- **File Upload**: Users can upload PDF files, which are processed and stored using FastAPI.
- **Query Handling**: FastAPI endpoints manage user queries, retrieve relevant data from the vector store, and provide responses using the Gemini Flash model.
- **Chat History Management**: Stores and retrieves chat history, allowing users to view past interactions.
- **Seamless Integration**: Ensures smooth communication between the backend and frontend, providing a cohesive user experience.

## Installation

To install the necessary dependencies, run:

```bash
pip install -r requirements.txt

