import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.docstore.document import Document
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

class LLM:
    def __init__(self, api_key=None):
        if api_key:
            os.environ['GOOGLE_API_KEY'] = api_key
        elif os.getenv('GOOGLE_API_KEY'):
            pass
        else:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
        
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

class FileModel(LLM):
    def __init__(self, course_file_dir='course_files/', api_key=None):
        super().__init__(api_key)
        self.course_file_dir = course_file_dir
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.db = None
        self.files = []

    def save_content_from_upload(self, uploaded_files):
        """Save uploaded files to course_file_dir"""
        saved_files = []
        for uploaded_file in uploaded_files:
            file_path = os.path.join(self.course_file_dir, uploaded_file.name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, "wb") as fp:
                fp.write(uploaded_file.getvalue())
            saved_files.append(file_path)
        return saved_files

    def load_text_to_db(self, text):
        """Load text content to vector database"""
        doc = Document(page_content=text)
        db = FAISS.from_documents([doc], self.embeddings)
        if self.db:
            self.db.merge_from(db)
        else: 
            self.db = db

    def load_pdf_to_db(self, filepath):
        """Load PDF file to vector database"""
        loader = PyPDFLoader(filepath) 
        pages = loader.load_and_split()
        db = FAISS.from_documents(pages, self.embeddings)
        if self.db:
            self.db.merge_from(db)
        else: 
            self.db = db
        self.files.append(filepath)

    def load_markdown_to_db(self, filepath):
        """Load Markdown file to vector database"""
        loader = UnstructuredMarkdownLoader(filepath, mode="elements")
        doc = loader.load()
        db = FAISS.from_documents(doc, self.embeddings)
        if self.db:
            self.db.merge_from(db)
        else: 
            self.db = db
        self.files.append(filepath)

    def query_documents(self, query, k=5):
        """Query the vector database for relevant documents"""
        if self.db is None:
            return []
        docs = self.db.similarity_search(query, k=k)
        return docs 