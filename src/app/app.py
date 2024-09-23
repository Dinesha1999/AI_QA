import streamlit as st  

from src.utills import extract_text_pdf,extract_text_docx,extract,convert_chunks, text_embedding, generate_answer
from bs4 import BeautifulSoup

def main():  
    html_temp = """  
    <div style="background-color: #33acff; padding: 8px; margin-bottom: 25px;">  
    <h1 style="color: #000000; text-align: center;">AI Powered Q & A System</h1>  
    </div>  
    """  
    st.markdown(html_temp, unsafe_allow_html=True) 
    data='data.pdf'
    #st.write(dataaaaa)
    with open('data_convert.html','r') as file:
        html_content=file.read()
    soup=BeautifulSoup(html_content,'html.parser')
    soup_str=str(soup)
    text_data=soup_str
    #text_data=extract(data)
    chunks=convert_chunks(text_data)
    vector_db=text_embedding(chunks)
    #st.write(vector_db)
    query = st.text_input("Enter The Question")
    if st.button("Process"):
        if query:
            answer=generate_answer(vector_db, query)
            st.write(answer)
        else:
            st.write("Please Enter a Valid Question")
if __name__ == '__main__':  
    main()