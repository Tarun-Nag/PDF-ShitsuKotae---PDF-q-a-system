🧠 Flask RAG Chatbot using Groq + LangChain

This project is a Retrieval-Augmented Generation (RAG) chatbot built with Flask, LangChain, Groq, and FAISS.
It allows users to upload PDF files, process them into a searchable vector database, and then chat with an AI that answers questions based on the uploaded content.

🚀 Features

📄 Upload PDF documents

🧩 Convert and store them in a FAISS vector database

💬 Chat with the content using a Groq LLM

🔐 Securely load API keys from environment files (api.env)

🌐 Built using Flask web framework

🛠️ Tech Stack

Python 3.10+

Flask

LangChain

LangGraph

Groq API

HuggingFace Embeddings

FAISS Vector Store

⚙️ Installation and Setup
1. Clone the Repository
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

2. Create and Activate a Virtual Environment
python -m venv venv
venv\Scripts\activate     # On Windows
# OR
source venv/bin/activate  # On macOS/Linux

3. Install Dependencies
pip install -r requirements.txt


If you don’t have a requirements.txt yet, you can create one with:

pip freeze > requirements.txt

🔑 Environment Setup
1. Create a file named api.env in your project root:
GROQ_API_KEY=your_groq_api_key_here

and name it:

api.env

ps: use your own groq ai api key here in your_groq_api_key_here


▶️ Running the App

After setting up your api.env and installing dependencies:

python app.py


Then open your browser and go to:
👉 http://127.0.0.1:5000/
