import streamlit as st
import poem

st.title("Poem Generator")

user_input = st.text_input("Please enter the topic of the poem or genre")

if st.button("Generate Poem"):
    genre = user_input.strip()  # Get the user input and remove leading/trailing spaces
    if genre:
        response = poem.poem(genre)
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