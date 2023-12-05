from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.chains import SequentialChain
from secret_key import openapi_key
import os


os.environ['OPENAI_API_KEY'] = openapi_key



#defining a function so that it can generate peom based on genre
def poem(genre):
    # making the model to suggest some poem title
    llm_name = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.7)
    name_template = """ Please suggest some poem title based on {genre} genre. Return only one output
    """
    poem_prompt_template = PromptTemplate(input_variables=['genre'], template=name_template)
    poem_chain = LLMChain(llm=llm_name, prompt=poem_prompt_template, output_key="title")

    # asking the model to generate poem based on the poem title
    llm_ideas = ChatOpenAI(model_name='gpt-3.5-turbo-16k', temperature=0.9)
    ideas_template = """Write the poem based on this {title}\
    in the style of "John Keats". \
    Make sure the poem is lovely and having deep meaning.
    Output the poem with just its content without mentioning the book title or any other information.\
    Output the poem in the following format:
    "<Insert the content of the poem here without reiterating 'poem' or mentioning the 'Title'>"
    """

    ideas_prompt_template = PromptTemplate(input_variables=['title'], template=ideas_template)
    ideas_chain = LLMChain(llm=llm_ideas, prompt=ideas_prompt_template, output_key="poem")

    # chaining the model chain together to get the desired output
    overall_chain = SequentialChain(
        chains=[poem_chain, ideas_chain],
        input_variables=['genre'],
        output_variables=['title', 'poem'],
        verbose=True
    )
    response = overall_chain({'genre': genre})

    return response

if __name__ == "__main__":
    print(poem("romance"))