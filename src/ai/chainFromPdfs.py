import time
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from icecream import ic
from concurrent.futures import ThreadPoolExecutor






# loading documents from folder
def loadPdfDocsFromFolder():
    ic("loadPdfDocsFromFolder")

    batch_docs= []

    src_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ic(src_path)

    
    folder_name = os.path.join(src_path, "src/data/pdfs")

    for root, dirs, files in os.walk(folder_name):
        for file in files:
            if file.endswith(".pdf"):
                # Do something with the PDF file, e.g. print its path
                ic(os.path.join(root, file))
                fName = os.path.join(root, file)
                ic(fName)

                pdf_loader = PyPDFLoader(fName)
                batch_docs.extend(pdf_loader.load())

    return batch_docs


    
# multiple file loading - load multiple files from pdf folder
def loadPdfDocsFromFolderWithMultithreadingAndBatchProcessing():
    ic("loadPdfDocsFromFolderWithMultithreadingAndBatchProcessing")

    src_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ic(src_path)

    
    root_directory = os.path.join(src_path, "src/data/pdfs")



    # Set the batch size (number of files to process in each batch)
    batch_size = 100

    # Initialize an empty list to store loaded documents
    docs = []

    # Function to process a batch of PDF files
    def process_pdf_batch(pdf_files):
        ic("process_pdf_batch")
        batch_docs = []
        for pdf_file_path in pdf_files:
            pdf_loader = PyPDFLoader(pdf_file_path)
            batch_docs.extend(pdf_loader.load())
        return batch_docs

    # Get the list of PDF files to process
    pdf_files_to_process = []
    for root, dirs, files in os.walk(root_directory):
        pdf_files_to_process.extend([os.path.join(root, file) for file in files if file.lower().endswith(".pdf")])

    # Create a ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        total_files = len(pdf_files_to_process)
        processed_files = 0

        # Iterate through the PDF files in batches
        for i in range(0, total_files, batch_size):
            batch = pdf_files_to_process[i:i+batch_size]
            batch_docs = list(executor.map(process_pdf_batch, [batch]))
            for batch_result in batch_docs:
                docs.extend(batch_result)
                processed_files += len(batch)
                ic(f"Processed {processed_files} / {total_files} files")
    
    #ic(len(docs))

    return docs



# split documents:
def splitDocs(docs):
    ic("splitDocuments")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    return splits



def storeSplitsIntoVectorDatabase_Chroma(splits):
    ic("storeSplitsIntoVectorDatabase_Chroma")

    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever() # Retriever is Runnable
    return retriever



# function that returns a chain
def getRAGChain():
    ic("getRAGChain")
    
    llm = ChatGroq(model = "llama-3.1-70b-versatile")
    docs = loadPdfDocsFromFolderWithMultithreadingAndBatchProcessing()
    splits = splitDocs(docs=docs)
    retriever = storeSplitsIntoVectorDatabase_Chroma(splits=splits)

    # little helper function for parsing docs
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    prompt_template = """
        You are an diabetic guru with many expertise in preparing delicious and healthy recepies..

        Context:
        {context}

        Question:
        {question}

        Please provide a detailed and accurate answer based on the given context.
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)

    rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()

    )

    return rag_chain


if __name__ == "__main__":
    
    chain = getRAGChain()
    ic(chain.invoke("Please provide 3 receipes for healthy breakfast?"))

