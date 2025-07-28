from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

class MadLibModel:
    def __init__(self, name, descriptions, placeholders, variables, template, **kwargs):
        self.name = name
        self.descriptions = descriptions
        self.placeholders = placeholders
        self.variables = variables
        self.values = ['' for i in range(len(variables))]
        self.human_template = template
        
        # Default identities
        self.bot_identity = "You are a helpful tutor."
        self.human_identity = "I am a student"
        self.bot_template = ""
        
        # Initialize prompts
        self.update_bot_identity(self.bot_identity)
        self.update_human_identity(self.human_identity)
    
    def update_bot_identity(self, new_identity):
        """Update bot identity and regenerate prompt"""
        self.bot_identity = new_identity
        self.bot_message_prompt = SystemMessagePromptTemplate.from_template(
            "\n\n".join([self.bot_identity, self.bot_template])
        )

    def update_bot_template(self, new_template):
        """Update bot template and regenerate prompt"""
        self.bot_template = new_template
        self.bot_message_prompt = SystemMessagePromptTemplate.from_template(
            "\n\n".join([self.bot_identity, self.bot_template])
        )
    
    def update_human_identity(self, new_identity):
        """Update human identity and regenerate prompt"""
        self.human_identity = new_identity
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(
            "\n\n".join([self.human_identity, self.human_template])
        )
    
    def get_formatted_prompt(self):
        """Get the formatted prompt with current values"""
        chat_prompt = ChatPromptTemplate.from_messages([
            self.bot_message_prompt, 
            self.human_message_prompt
        ])
        
        kwargs = {key: value for key, value in zip(self.variables, self.values)}
        return chat_prompt.format_prompt(**kwargs)
    
    def set_values(self, values):
        """Set values for the madlib variables"""
        if len(values) != len(self.variables):
            raise ValueError(f"Expected {len(self.variables)} values, got {len(values)}")
        self.values = values 