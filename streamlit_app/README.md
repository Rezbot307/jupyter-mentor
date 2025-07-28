# Jupyter Mentor AI - Streamlit App

A Streamlit-based educational AI chatbot system that replicates the functionality of the original Jupyter notebook application.

## Features

- **Role-based interfaces**: Different experiences for students and educators
- **Template-driven conversations**: Structured prompts for consistent AI responses
- **Document integration**: Upload and process course materials (PDF/Markdown)
- **Vector search**: Semantic document retrieval capabilities
- **Multiple conversation modes**: Open prompt, metaphor, step-by-step, debate partner, translation, quiz generation

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Google Gemini API key**:
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Set it as an environment variable: `export GOOGLE_API_KEY=your_api_key`
   - Or enter it in the app's sidebar

3. **Run the app**:
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Select your role** (Student or Educator) in the sidebar
2. **Enter your Google Gemini API key** in the sidebar
3. **Navigate through the tabs**:
   - **Login**: Enter your username
   - **Profile**: Fill in your profile information
   - **Course Overview**: Upload/download course files
   - **Chatbot**: Interact with the AI tutor

## Conversation Modes

### Student Modes:
- **Open Prompt**: Free-form conversation
- **Metaphor**: Explain concepts using metaphors
- **Step-by-Step**: Break down complex topics
- **Debate Partner**: Socratic method debates

### Educator Modes:
- **Open Prompt**: Free-form conversation
- **Metaphor**: Explain concepts using metaphors
- **Translate**: Translate text into different languages
- **Quiz Questions**: Generate quiz questions about topics

## File Structure

```
streamlit_app/
├── app.py              # Main Streamlit application
├── llm.py              # LLM integration with Google Gemini
├── madlib.py           # Template-based prompt system
├── chatbot.py          # Chatbot model and logic
├── constants.py        # Madlib templates and constants
├── utils.py            # Utility functions
├── requirements.txt    # Python dependencies
├── uploaded_files/     # Directory for uploaded course files
└── README.md          # This file
```

## Technical Details

- **LLM**: Google Gemini 1.5 Flash
- **Vector Database**: FAISS for document embeddings
- **Document Processing**: PDF and Markdown support
- **UI Framework**: Streamlit
- **State Management**: Streamlit session state 