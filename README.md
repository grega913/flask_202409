# 20241004 - adding a

# 20241003 - adding new route for pdfs loading from a folder - gg (glucose goddess)

## relevant files:

- ai/gg.py
- routes.py -> new route defined: gg
- templates/gg.html -> html template for displaying relevant data
- static/gg.js -> js for gg.html template

# 20241003 - working route is "/chat"

# 20241002 - Should be working, but the fact that all the db gets called everytime a LLM request is made, quickly fills the context. Should be fixed.

# 20241002 - added tts to chat.js, so that messages are read. Had quite some problems with definig paths in route/chat, but made it work with fetch after all.

test_persistance.py --> added memory logic, with SQAlchemy and sqlite.

# flask_202409

Training with Flask, LLMs, Chats, LangChain, ChatGroq, VoiceControl

# How to run?

python main.py
