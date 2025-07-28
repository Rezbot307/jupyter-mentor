from madlib import MadLibModel
from llm import FileModel
from langchain_core.prompts.chat import ChatPromptTemplate

class ChatBotModel(FileModel):
    def __init__(self, madlibs_list, course_file_dir='course_files/', api_key=None):
        super().__init__(course_file_dir, api_key)
        self.names = []
        self.madlib_models = []
        for value in madlibs_list:
            model = MadLibModel(**value)
            self.names.append(model.name)
            self.madlib_models.append(model)
        self.selected_index = 0

    def set_selected_index(self, idx):
        self.selected_index = idx

    def set_madlib_values(self, values):
        self.madlib_models[self.selected_index].set_values(values)

    def prompt(self):
        madlib = self.madlib_models[self.selected_index]
        prompt = madlib.get_formatted_prompt()
        response = self.llm.invoke(prompt)
        interm = [desc + ' ' + val for desc, val in zip(madlib.descriptions, madlib.values)]
        user = "\n".join(interm)
        return user, response.content

    def prompt_with_kwargs(self, kwargs):
        madlib = self.madlib_models[self.selected_index]
        prompt = madlib.get_formatted_prompt(**kwargs)
        response = self.llm.invoke(prompt)
        return response.content

    def prompt_course_files(self, input_text):
        """Answer questions based on uploaded course documents"""
        if self.db:
            try:
                docs = self.db.similarity_search(input_text, k=1)
                docs_content = " ".join([d.page_content for d in docs])
                
                # Create a prompt that includes the course content
                system_prompt = f"You are a helpful tutor. Answer the question based on the following course information: {docs_content}"
                human_prompt = f"Question: {input_text}"
                
                chat_prompt = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    ("human", human_prompt)
                ])
                
                response = self.llm.invoke(chat_prompt.format_prompt())
                return f"{response.content}\n\nSourced from course materials."
            except Exception as e:
                return f"Error querying documents: {str(e)}"
        else:
            # Fall back to regular prompt if no documents are loaded
            return self.prompt()[1]  # Return just the bot response 