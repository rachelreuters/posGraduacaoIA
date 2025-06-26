

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

class GetNotesTemplate:
    def __init__(self):
        self.system_template = """
        You are a perfumist and you will tell the user the type and all the notes from the perfume the user inputs.

        Your output must be the list of strings, where will put the type in portugues and the notes also in portuguese. 
        For example the output must be something like : "Floral, Baunilha, Fava Tonka, Mandarina"
        """

        self.human_template = """
        #### {request}
        """
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(self.system_template)
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(self.human_template)
        self.chat_prompt = ChatPromptTemplate.from_messages([self.system_message_prompt,
                                                             self.human_message_prompt])
