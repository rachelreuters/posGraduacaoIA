

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

class GetSimilarPerfumesTemplate:
    def __init__(self):
        self.system_template = """
        You are a perfumist and you will tell the user a list of 6 perfumes that are similar to the list of type and notes the user wants, 
        DO NOT include the original perfume in the list.
        Remove the original perfume the user input from the list!

        Your final output must be the list of 6 perfume names and the name of perfumist in portuguese (different than the original perfume). 
        If the name of perfume is close to original input, DO NOT INCLUDE in the list.
        For example the output must be something like : "Scandal Jean Paul Gaultier"
        """

        self.human_template = """
        #### {request}
        """
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(self.system_template)
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(self.human_template)
        self.chat_prompt = ChatPromptTemplate.from_messages([self.system_message_prompt,
                                                             self.human_message_prompt])
