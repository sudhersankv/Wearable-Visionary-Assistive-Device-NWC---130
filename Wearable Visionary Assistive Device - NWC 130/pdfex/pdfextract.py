import PyPDF2
from PyPDF2 import PdfReader

from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import textwrap
import glob

OPENAI_API_KEY = "YOURAPIKEY"
               

    

load_dotenv(find_dotenv())
embeddings = OpenAIEmbeddings(openai_api_key= OPENAI_API_KEY)

def extract_text_from_pdf(pdf_file):
        pdfreader = PdfReader(pdf_file)
        from typing_extensions import Concatenate
        # read text from pdf
        pdf_text = ''
        for i, page in enumerate(pdfreader.pages):
            content = page.extract_text()
            if content:
                pdf_text += content
        return pdf_text
    
def create_db_from_pdf(pdf_text):
    
    text_splitter = CharacterTextSplitter(separator= '\n', chunk_size = 800, chunk_overlap = 200, length_function = len)
    texts = text_splitter.split_text(pdf_text)
    
    db = FAISS.from_texts(texts, embeddings)
    return db    


pdfreader = PdfReader('sample.pdf')

from typing_extensions import Concatenate
# read text from pdf
raw_text = ''
for i, page in enumerate(pdfreader.pages):
    content = page.extract_text()
    if content:
        raw_text += content


def get_response_from_pdf(db, query, k=4):
    docs = db.similarity_search(query, k=k)
    docs_page_content = ' '.join([d.page_content for d in docs])
    
    chat = ChatOpenAI(model_name = 'gpt-3.5-turbo-16k', temperature = 0.2, openai_api_key = OPENAI_API_KEY)
    
    # template for the system message prompt
    template = """
  You are a helpful assistant that can answer questions about PDFs for blind people based on the document content: {docs}
  
  Only use the factual information from the document to answer the question.
  
  If you feel like you don't have enough information to answer it, say 'I am not sure about that.'
  
  Talk like you are speaking with a blind person without them knowing you are showing sympathy or compassion.

  if query is either bye or thank you, respond with "Bye Master, I'm always at your service!" 
"""


    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    
    # Human question prompt
    human_template = ' Answer the following question: {question}'
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    
    chain = LLMChain(llm = chat, prompt = chat_prompt)
    
    response = chain.run(question = query, docs = docs_page_content)
    response = response.replace('\n','')
    return response, docs