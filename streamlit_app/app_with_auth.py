import streamlit as st
from constants import student_madlibs, educator_madlibs
from chatbot import ChatBotModel
from utils import check_api_key, is_pdf, is_markdown, save_uploaded_file
import os

st.set_page_config(page_title="Jupyter Mentor AI", layout="wide")

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def login_page():
    """Display the login page"""
    st.title("🎓 Jupyter Mentor AI")
    st.markdown("---")
    
    # Create a centered login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Login")
        
        # API Key input
        api_key = st.text_input("Google Gemini API Key", type="password", 
                               help="Enter your Google Gemini API key")
        
        # Username input
        username = st.text_input("Username", placeholder="Enter your username")
        
        # Role selection
        role = st.selectbox("Select your role", ["Student", "Educator"])
        
        # Login button
        if st.button("Login", type="primary", use_container_width=True):
            if not username:
                st.error("Please enter a username.")
            elif not api_key:
                st.error("Please enter your Google Gemini API key.")
            else:
                # Test API key
                try:
                    # Quick test of API key
                    test_model = ChatBotModel([], api_key=api_key)
                    st.session_state['authenticated'] = True
                    st.session_state['user_role'] = role
                    st.session_state['username'] = username
                    st.session_state['api_key'] = api_key
                    st.success("Login successful!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Invalid API key or connection error: {str(e)}")
        
        # Help text
        st.markdown("---")
        st.markdown("""
        **Need an API key?**
        1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Create a new API key
        3. Copy and paste it above
        """)

def main_app():
    """Display the main application after login"""
    
    # Sidebar with user info and logout
    with st.sidebar:
        st.title("🎓 Jupyter Mentor AI")
        st.markdown(f"**Welcome, {st.session_state['username']}!**")
        st.markdown(f"**Role:** {st.session_state['user_role']}")
        
        if st.button("Logout"):
            st.session_state['authenticated'] = False
            st.session_state['user_role'] = None
            st.session_state['username'] = None
            st.session_state['api_key'] = None
            st.rerun()
        
        st.markdown("---")
    
    # Main tabs
    tabs = ["Profile", "Course Overview", "Chatbot"]
    tab1, tab2, tab3 = st.tabs(tabs)
    
    # Profile Tab
    with tab1:
        st.header("User Profile")
        if st.session_state['user_role'] == "Student":
            with st.form("student_profile_form"):
                name = st.text_input("Name", value=st.session_state.get('profile_name', ''))
                school = st.text_input("School", value=st.session_state.get('profile_school', ''))
                year = st.selectbox("Grade Level", ["Freshman", "Sophomore", "Junior", "Senior"], 
                                  index=["Freshman", "Sophomore", "Junior", "Senior"].index(st.session_state.get('profile_year', 'Freshman')))
                major = st.text_input("Major", value=st.session_state.get('profile_major', ''))
                minors = st.text_input("Minors/Certificates", value=st.session_state.get('profile_minors', ''))
                interests = st.text_input("Outside Interests", value=st.session_state.get('profile_interests', ''))
                
                if st.form_submit_button("Save Profile"):
                    st.session_state['profile_name'] = name
                    st.session_state['profile_school'] = school
                    st.session_state['profile_year'] = year
                    st.session_state['profile_major'] = major
                    st.session_state['profile_minors'] = minors
                    st.session_state['profile_interests'] = interests
                    st.success("Profile saved successfully!")
        else:
            with st.form("educator_profile_form"):
                name = st.text_input("Name", value=st.session_state.get('profile_name', ''))
                level = st.selectbox("Educator Level", ["Elementary School", "Middle School", "High School", "College"],
                                   index=["Elementary School", "Middle School", "High School", "College"].index(st.session_state.get('profile_level', 'Elementary School')))
                
                if st.form_submit_button("Save Profile"):
                    st.session_state['profile_name'] = name
                    st.session_state['profile_level'] = level
                    st.success("Profile saved successfully!")
    
    # Course Overview Tab
    with tab2:
        st.header("Course Overview")
        course_file_dir = "uploaded_files"
        
        if st.session_state['user_role'] == "Educator":
            st.subheader("Upload Course Files (PDF/Markdown)")
            uploaded_files = st.file_uploader("Upload files", type=["pdf", "md"], accept_multiple_files=True)
            if uploaded_files:
                # Create chatbot model for file processing
                madlibs = educator_madlibs
                file_processing_model = ChatBotModel(madlibs, course_file_dir=course_file_dir, api_key=st.session_state['api_key'])
                
                for uploaded_file in uploaded_files:
                    file_path = save_uploaded_file(uploaded_file, course_file_dir)
                    st.success(f"Saved: {uploaded_file.name}")
                    
                    # Process uploaded files into vector database
                    try:
                        if uploaded_file.name.lower().endswith('.pdf'):
                            file_processing_model.load_pdf_to_db(file_path)
                        elif uploaded_file.name.lower().endswith('.md'):
                            file_processing_model.load_markdown_to_db(file_path)
                        st.success(f"Processed {uploaded_file.name} into knowledge base")
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {str(e)}")
            
            st.subheader("Course Settings")
            course_overview = st.text_area("Course Overview", value=st.session_state.get('course_overview', ''))
            ai_guidelines = st.text_area("AI Guidelines", value=st.session_state.get('ai_guidelines', ''))
            
            col1, col2 = st.columns(2)
            with col1:
                step_by_step = st.checkbox("Step-by-Step", value=st.session_state.get('step_by_step', False))
                metaphor = st.checkbox("Metaphor", value=st.session_state.get('metaphor', False))
            with col2:
                hints = st.checkbox("Hints", value=st.session_state.get('hints', False))
                ai_guided = st.checkbox("AI Guided Questions", value=st.session_state.get('ai_guided', False))
            
            open_ended = st.text_area("Open-ended Response", value=st.session_state.get('open_ended', ''))
            
            if st.button("Save Course Settings"):
                st.session_state['course_overview'] = course_overview
                st.session_state['ai_guidelines'] = ai_guidelines
                st.session_state['step_by_step'] = step_by_step
                st.session_state['metaphor'] = metaphor
                st.session_state['hints'] = hints
                st.session_state['ai_guided'] = ai_guided
                st.session_state['open_ended'] = open_ended
                st.success("Course settings saved!")
        else:
            st.subheader("Download Course Files")
            if os.path.exists(course_file_dir):
                files = os.listdir(course_file_dir)
                if files:
                    for file in files:
                        file_path = os.path.join(course_file_dir, file)
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label=f"📄 Download {file}",
                                data=f.read(),
                                file_name=file,
                                mime="application/octet-stream"
                            )
                else:
                    st.info("No course files available for download.")
            else:
                st.info("No course files uploaded yet.")
    
    # Chatbot Tab
    with tab3:
        st.header("AI Chatbot")
        
        # Get appropriate madlibs based on role
        madlibs = student_madlibs if st.session_state['user_role'] == "Student" else educator_madlibs
        chatbot_model = ChatBotModel(madlibs, course_file_dir=course_file_dir, api_key=st.session_state['api_key'])
        
        # Add course-aware chat option
        chat_modes = ["Course-Aware Chat"] + [m['name'] for m in madlibs]
        selected_mode = st.selectbox("Select Chat Mode", chat_modes)
        
        if selected_mode == "Course-Aware Chat":
            # Course-aware chat interface
            st.subheader("Ask questions about your course materials")
            user_question = st.text_input("Ask a question about your course:", placeholder="e.g., When will we learn about integration?")
            
            if st.button("Ask Question"):
                if user_question:
                    response = chatbot_model.prompt_course_files(user_question)
                    st.session_state['chat_history'].append((user_question, response))
                    st.rerun()
                else:
                    st.warning("Please enter a question.")
            
            # Display course-aware chat history
            if st.session_state['chat_history']:
                st.subheader("Course Q&A History")
                for i, (question, answer) in enumerate(st.session_state['chat_history']):
                    with st.expander(f"Q&A {i+1}", expanded=True):
                        st.markdown(f"**❓ Question:** {question}")
                        st.markdown(f"**🤖 Answer:** {answer}")
        else:
            # Regular madlib-based chat
            madlib_names = [m['name'] for m in madlibs]
            selected = madlib_names.index(selected_mode)
            chatbot_model.set_selected_index(selected)
            madlib = chatbot_model.madlib_models[selected]
            
            # Dynamic input form for madlib modes
            with st.form("chatbot_form"):
                st.subheader(f"Mode: {selected_mode}")
                values = []
                for i, (desc, placeholder) in enumerate(zip(madlib.descriptions, madlib.placeholders)):
                    if desc:  # Only show input if there's a description
                        val = st.text_input(f"{desc}", placeholder=placeholder, key=f"input_{i}")
                    else:
                        val = st.text_input("Message", placeholder=placeholder, key=f"input_{i}")
                    values.append(val)
                
                if st.form_submit_button("Send Message"):
                    if any(values):  # Check if any input is provided
                        chatbot_model.set_madlib_values(values)
                        user, bot = chatbot_model.prompt()
                        st.session_state['chat_history'].append((user, bot))
                        st.rerun()
                    else:
                        st.warning("Please enter some text before sending.")
            
            # Display chat history for madlib modes
            if st.session_state['chat_history']:
                st.subheader("Chat History")
                for i, (user, bot) in enumerate(st.session_state['chat_history']):
                    with st.expander(f"Conversation {i+1}", expanded=True):
                        st.markdown(f"**👤 User:** {user}")
                        st.markdown(f"**🤖 AI:** {bot}")
                
                if st.button("Clear Chat History"):
                    st.session_state['chat_history'] = []
                    st.rerun()

# Main app logic
if not st.session_state['authenticated']:
    login_page()
else:
    main_app() 