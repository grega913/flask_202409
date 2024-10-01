
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from icecream import ic


DATABASE_URL = "sqlite:///chat_history.db"
Base = declarative_base()



store={}


class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    session_id = Column(String, unique=True, nullable=False)
    messages = relationship("Message", back_populates="session")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    session = relationship("Session", back_populates="messages")

def print_message_info(message):
    print(f"ID: {message.id}, Session ID: {message.session_id}, Role: {message.role}, Content: {message.content}")

def print_session_info(session):
    print(f"ID: {session.id}, Session ID: {session.session_id}")


# Create the database and the tables
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to save a single message
def save_message(session_id: str, role: str, content: str):

    ic((session_id) + " " + (role) + " " + (content) )

    db = next(get_db())
    try:
        session = db.query(Session).filter(Session.session_id == session_id).first()
        if not session:
            session = Session(session_id=session_id)
            db.add(session)
            db.commit()
            db.refresh(session)

        db.add(Message(session_id=session.id, role=role, content=content))
        db.commit()
    except SQLAlchemyError:
        db.rollback()
    finally:
        db.close()

# Function to load chat history
def load_session_history(session_id: str) -> BaseChatMessageHistory:
    db = next(get_db())
    chat_history = ChatMessageHistory()
    try:
        session = db.query(Session).filter(Session.session_id == session_id).first()
        if session:

            print_session_info(session)
            for message in session.messages:
                print_message_info(message=message)

                chat_history.add_message({"role": message.role, "content": message.content})
    except SQLAlchemyError:
        pass
    finally:
        db.close()

    return chat_history



# Ensure you save the chat history to the database when needed
def save_all_sessions():
    for session_id, chat_history in store.items():
        for message in chat_history.messages:
            save_message(session_id, message["role"], message["content"])

# Example of saving all sessions before exiting the application
import atexit
atexit.register(save_all_sessions)


def get_chain_with_message_history_2():

    print("get_chain_with_message_history_2")

    #model = ChatGroq()
    model = ChatOpenAI()

    chat_history = ChatMessageHistory()

    session_id=[] 

    prompt = ChatPromptTemplate.from_messages(
        [
            (
            "system", "You are a helpful assistant. Answer all questions to the best of your ability. The provided chat history includes facts about the user you are speaking with.",
            ),
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
        ]
    )

    chain = prompt | model


    # Modify the get_session_history function to use the database
    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = load_session_history(session_id)
        return store[session_id]
    

    chain_with_message_history_2 = RunnableWithMessageHistory(
        chain,
        #lambda session_id: chat_history,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )


    return chain_with_message_history_2




def invoke_and_save(chain, session_id, input_text):
    # Save the user question with role "human"

    ic("invoke and save")
    ic(session_id)
    ic(input_text)

    save_message(session_id, "human", input_text)
    
    result = chain.invoke(
        {"input": input_text},
        config={"configurable": {"session_id": session_id}}
    )

    print(result)

    answer = result.content

    # Save the AI answer with role "ai"
    save_message(session_id, "ai", answer)
    return answer


