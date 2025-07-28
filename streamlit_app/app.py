import streamlit as st
from constants import student_madlibs, educator_madlibs
from chatbot import ChatBotModel
from utils import check_api_key, is_pdf, is_markdown, save_uploaded_file
import os

st.set_page_config(page_title="Jupyter Mentor AI", layout="wide")

# --- Sidebar for role selection and API key ---
st.sidebar.title("Jupyter Mentor AI")
role = st.sidebar.selectbox("Select your role", ["Student", "Educator"])
st.sidebar.markdown("---")
api_key = st.sidebar.text_input("Google Gemini API Key", type="password")
if api_key:
    st.session_state['api_key'] = api_key

# --- Tabs ---
tabs = ["Login", "Profile", "Course Overview", "Chatbot"]
tab1, tab2, tab3, tab4 = st.tabs(tabs)

# --- Shared session state ---
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# --- Login Tab ---
with tab1:
    st.header("Login")
    username = st.text_input("Username")
    if st.button("Login"):
        if not username:
            st.warning("Please enter a username.")
        elif not check_api_key():
            pass
        else:
            st.success(f"Welcome, {username}!")
            st.session_state['username'] = username

# --- Profile Tab ---
with tab2:
    st.header("User Profile")
    if role == "Student":
        name = st.text_input("Name")
        school = st.text_input("School")
        year = st.selectbox("Grade Level", ["Freshman", "Sophomore", "Junior", "Senior"]) 
        major = st.text_input("Major")
        minors = st.text_input("Minors/Certificates")
        interests = st.text_input("Outside Interests")
        if st.button("Save Profile", key="student_profile"):
            st.success("Profile saved!")
            st.session_state['profile'] = {
                'name': name, 'school': school, 'year': year, 'major': major, 'minors': minors, 'interests': interests
            }
    else:
        name = st.text_input("Name")
        level = st.selectbox("Educator Level", ["Elementary School", "Middle School", "High School", "College"])
        if st.button("Save Profile", key="educator_profile"):
            st.success("Profile saved!")
            st.session_state['profile'] = {'name': name, 'level': level}

# --- Course Overview Tab ---
with tab3:
    st.header("Course Overview")
    course_file_dir = "uploaded_files"  # Use a separate folder for uploads
    if role == "Educator":
        st.subheader("Upload Course Files (PDF/Markdown)")
        uploaded_files = st.file_uploader("Upload files", type=["pdf", "md"], accept_multiple_files=True)
        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_path = save_uploaded_file(uploaded_file, course_file_dir)
                st.success(f"Saved: {uploaded_file.name}")
        st.text_area("Course Overview")
        st.text_area("AI Guidelines")
        st.checkbox("Step-by-Step")
        st.checkbox("Metaphor")
        st.checkbox("Hints")
        st.checkbox("AI Guided Questions")
        st.text_area("Open-ended Response")
    else:
        st.subheader("Download Course Files")
        files = os.listdir(course_file_dir) if os.path.exists(course_file_dir) else []
        for file in files:
            st.download_button(
                label=f"Download {file}",
                data=open(os.path.join(course_file_dir, file), "rb").read(),
                file_name=file
            )

# --- Chatbot Tab ---
with tab4:
    st.header("AI Chatbot")
    madlibs = student_madlibs if role == "Student" else educator_madlibs
    chatbot_model = ChatBotModel(madlibs, course_file_dir=course_file_dir, api_key=st.session_state.get('api_key'))
    madlib_names = [m['name'] for m in madlibs]
    selected = st.selectbox("Select Chatbot Mode", madlib_names)
    idx = madlib_names.index(selected)
    chatbot_model.set_selected_index(idx)
    madlib = chatbot_model.madlib_models[idx]
    # Dynamic input fields for madlib variables
    values = []
    for desc, placeholder in zip(madlib.descriptions, madlib.placeholders):
        val = st.text_input(desc, placeholder=placeholder)
        values.append(val)
    if st.button("Send Message"):
        chatbot_model.set_madlib_values(values)
        user, bot = chatbot_model.prompt()
        st.session_state['chat_history'].append((user, bot))
    # Display chat history
    for user, bot in st.session_state['chat_history']:
        st.markdown(f"**USER:** {user}")
        st.markdown(f"**CHATBOT:** {bot}") 