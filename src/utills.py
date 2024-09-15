import PyPDF2
from docx import Document
from dotenv import load_dotenv,find_dotenv
import openai
import os
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
load_dotenv(find_dotenv())
api_key=os.environ.get("OPEN_API_KEY")
embedding=OpenAIEmbeddings(openai_api_key=api_key)
llm = OpenAI(api_key=api_key)
# extract text from PDF document
def extract_text_pdf(pdf):
    text = ""
    reader = PyPDF2.PdfReader(pdf)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# extract text from docx
def extract_text_docx(docx):
    doc = Document(docx)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# extract handle
def extract(doc):
    _, file_extension = doc.split('.')
    print(file_extension)
    if file_extension == 'pdf':
        return extract_text_pdf(doc)
    elif file_extension == 'docx':
        return extract_text_docx(doc)
    else:
        raise ValueError("Unsupported file format")


## Divide Document into chunks


def convert_chunks(text_data):
    text_splitter=CharacterTextSplitter(
    separator="\n",
    chunk_size=1500,
    chunk_overlap=300,
    length_function=len,
    )
    chunks=text_splitter.split_text(text_data)
    return chunks





def text_embedding(chunks):

    if os.path.exists("vectorstore/index.pkl"):
    # Load the existing vector store
        db = FAISS.load_local("vectorstore", embedding,allow_dangerous_deserialization=True)
    else:
    # Create a new vector store from the text chunks
        db = FAISS.from_texts(texts=chunks, embedding=embedding)
    # Save the newly created vector store locally
    db.save_local("vectorstore")
    return db

def generate_answer(vector_db,query):
    embedding_vector = embedding.embed_query(query)
    docs = vector_db.similarity_search_by_vector(embedding_vector)
    print(docs[0])
    print(docs[1])
 
    chain=load_qa_chain(llm=llm,chain_type='stuff')
    response= chain.run(input_documents=docs,question=query)

    return response


def soup(data): # to extract html data
    pass