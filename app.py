import streamlit as st
import ast
from langchain.tools import YouTubeSearchTool
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

st.set_page_config(page_title="Insightful Streams")
st.title("Insightful Streams")
st.write("Dive deeper into any topic with a crafted info and handpicked videos.")

# Create States
initialStates = {
    'api_key': '',
    'key_validation': False
}
for key, value in initialStates.items():
    if key not in st.session_state:
        st.session_state[key] = value

with st.sidebar:
    st.title("API Key")
    api = st.text_input("Please add your API key", type="password")
    validate = st.button("Validate API")

    if validate:
        if api.startswith("sk-"):
            st.session_state['api_key'] = api
            st.session_state['key_validation'] = True
        elif not api.startswith('sk-'):
            st.write("Please add a valid API Key")
        else:
            st.write("Please an API Key")


with st.container():
    if st.session_state['key_validation']:
        keyword = st.text_input("Enter your keyword")
        if keyword:
            # Generate a text/paragraph about the input using the Langchain API
            prompt_template = PromptTemplate(
                input_variables=["keyword"],
                template="Write a paragraph about {keyword}"
            )

            llm = OpenAI(verbose=True, temperature=0.9, openai_api_key=st.session_state['api_key'])
            chain = LLMChain(llm=llm, prompt=prompt_template)

            paragraph = chain.run(keyword)

            # Display the generated paragraph
            st.write(paragraph)

            # Fetch the YouTube videos related to the input
            tool = YouTubeSearchTool()
            response = tool.run(keyword + ", 2")
            if response:
                st.subheader("Related Youtube Videos:")
                urlsList = ast.literal_eval(response)
                columns = st.columns(len(urlsList))
                for col, url in zip(columns, urlsList):
                    cleanUrl = url.split("&pp")[0]
                    finalUrl = cleanUrl.replace("watch?v=", "embed/")
                    col.markdown(f'<iframe width="100%" height="250px" src="{finalUrl}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)


