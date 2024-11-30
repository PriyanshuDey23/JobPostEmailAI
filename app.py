from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from prompt import *  
from utils import *

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables just like you would with os.environ
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Function to extract text from URL
# Initialize the WebBaseLoader
def extract_text_from_url(url: str) -> str:
    loader=WebBaseLoader(url)
    docs=loader.load()
    return docs


# Response Format For email gen
def email_chain(input_data):
    # Define the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", temperature=1, api_key=GOOGLE_API_KEY)  
    
    # Define the prompt
    PROMPT_TEMPLATE = PROMPT  # Imported from prompt.py
    prompt = PromptTemplate(
            input_variables=["input_data"],   # From prompt
            template=PROMPT_TEMPLATE,
        )
      
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Generate response
    response = llm_chain.run({"input_data": input_data})
    return response


# Set the streamlit app

st.set_page_config(page_title="JobPostEmailGenerator")
st.header("JobPostEmailGenerator")

# URL input
url = st.text_input("Enter the url of the job Posting")

# Generation Button:
if st.button("Generate"):
    url_text=extract_text_from_url(url=url)


    response=email_chain(input_data=url_text)
    st.subheader("Generated Email:")
    st.write(response)

    # Download button 
    st.download_button(
            label="Download as TXT",
            data=convert_to_txt(response),
            file_name="email.txt",
            mime="text/plain",
        )
    st.download_button(
            label="Download as DOCX",
            data=convert_to_docx(response),
            file_name="email.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )  





