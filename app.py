
from flask import Flask, request, render_template, redirect, url_for, session
import os
from langchain.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.agents.agent_toolkits import create_retriever_tool
from langgraph.prebuilt import create_react_agent
from langchain_groq.chat_models import ChatGroq
from dotenv import load_dotenv

load_dotenv(api.env)  

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session

UPLOAD_FOLDER = 'Data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize embedding model and LLM
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
llm = ChatGroq(
    model_name="mixtral-8x7b",
    temperature=0.1,
    api_key=os.getenv("GROQ_API_KEY")
)


os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def VectorDB(path):
    filename = os.path.splitext(os.path.basename(path))[0]
    loader = PyPDFLoader(path)
    docs = loader.load()
    vectorstore = FAISS.from_documents(docs, embedding=embedding_model)
    vectorstore.save_local(f'{UPLOAD_FOLDER}/DATA')
    return filename

def QNA(query):
    index = os.listdir(UPLOAD_FOLDER)[0]
    vectorstore = FAISS.load_local(f'{UPLOAD_FOLDER}/{index}', embeddings=embedding_model, allow_dangerous_deserialization=True)
    retriever_tool = create_retriever_tool(
        vectorstore.as_retriever(),
        name="VectorDB",
        description="Use this vector store tool to answer the user question"
    )
    agent = create_react_agent(
        model=llm,
        tools=[retriever_tool],
        prompt="You are a helpful RAG Agent. Answer based on Content provided . If content is not relevent and can't satisfy the question ask for more details."
    )
    response = agent.invoke({"messages":[query]})
    return response['messages'][-1].content

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            VectorDB(filepath)
            os.remove(filepath)
            return redirect(url_for('chat'))
    return render_template('upload.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'messages' not in session:
        session['messages'] = []

    if request.method == 'POST':
        user_message = request.form['message']
        bot_response = QNA(user_message)
        
        session['messages'].append(("user", user_message))
        session['messages'].append(("bot", bot_response))
        session.modified = True

    return render_template('chat.html', messages=session['messages'])

if __name__ == "__main__":
    app.run(debug=True)


