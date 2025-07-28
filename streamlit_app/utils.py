import os
import streamlit as st

def check_api_key():
    api_key = st.session_state.get('api_key') or os.getenv('GOOGLE_API_KEY')
    if not api_key:
        st.error('Please enter your Google Gemini API key.')
        return False
    return True

def is_pdf(filename):
    return filename.lower().endswith('.pdf')

def is_markdown(filename):
    return filename.lower().endswith('.md')

def save_uploaded_file(uploaded_file, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    return file_path 