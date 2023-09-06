import argparse
import os
import streamlit as st
from streamlit_chat import message
from utils.backend import load_embeddings_and_lines, similarity_search, answers_agent

def run_chat_app(repo_url):
    """Run the chat application using the Streamlit framework."""
    st.title("GitHUB GPT")

    file_name = "_".join(repo_url.split('/')[-2:]) + ".txt"
    embeddings, lines = load_embeddings_and_lines(file_name)

    # Initialize the session state for generated responses and past inputs
    if "generated" not in st.session_state:
        st.session_state["generated"] = ["i am ready to help you ser"]

    if "past" not in st.session_state:
        st.session_state["past"] = ["hello"]

    # Get the user's input from the text input field
    user_input = get_text()

    # If there is user input, search for a response using the search_db function
    if user_input:
        response_data = similarity_search(user_input, embeddings, lines)
        answer = answers_agent(user_input, response_data)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(answer)

    # If there are generated responses, display the conversation using Streamlit
    # messages
    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
            message(st.session_state["generated"][i], key=str(i))


#def generate_response(prompt):
#    """
#    Generate a response using OpenAI's ChatCompletion API and the specified prompt.
#    """
#    completion = openai.ChatCompletion.create(
#        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
#    )
#    response = completion.choices[0].message.content
#    return response

def get_text():
    """Create a Streamlit input field and return the user's input."""
    input_text = st.text_input("", key="input")
    return input_text

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-url", type=str, required=True)
    args = parser.parse_args()

    #run_chat_app(args.activeloop_dataset_path)
    run_chat_app(args.repo_url)
