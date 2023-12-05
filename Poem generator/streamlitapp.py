from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.chains import SequentialChain
import streamlit as st
import os


os.environ['OPENAI_API_KEY'] = "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"



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



st.title("Poem Generator")

user_input = st.text_input("Please enter the topic of the poem or genre")

if st.button("Generate Poem"):
    genre = user_input.strip()  # Get the user input and remove leading/trailing spaces
    if genre:
        response = poem(genre)
        if response:
            st.header(response['title'].strip())
            poem_lines = response['poem'].strip().split('\n\n')  # Split poem by empty lines
            for stanza in poem_lines:
                stanza_lines = stanza.split('\n')  # Split each stanza into lines
                formatted_stanza = '<p>' + '<br>'.join(stanza_lines) + '</p>'  # Join lines with <br> and wrap in <p> tags
                st.markdown(formatted_stanza, unsafe_allow_html=True)  # Display stanza preserving HTML
        else:
            st.error("Could not generate a poem for the entered genre. Please try a different one.")
    else:
        st.warning("Please enter a genre.")