from langchain.memory import ConversationBufferMemory,ConversationBufferWindowMemory
from langchain import PromptTemplate
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.embeddings import SentenceTransformerEmbeddings
from fastapi import FastAPI, Request, Form, Response,Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant
import os
import json
from datetime import datetime, timedelta 
# from textblob import TextBlob
from langchain.chains import ConversationChain
# from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.llms import HuggingFaceHub
from langchain.chains import ConversationalRetrievalChain
import csv
import datetime
import pytz
from langchain_community.llms import Ollama
import os
# from pymongo import MongoClient
# from bson.objectid import ObjectId
import json
# import mysql.connector
import re
import warnings
from typing import List
# import torch
from langchain import PromptTemplate
from langchain.chains import ConversationChain
from langchain.llms import HuggingFacePipeline
from langchain.schema import BaseOutputParser
from transformers import (AutoModelForCausalLM,AutoTokenizer,StoppingCriteria,StoppingCriteriaList,pipeline,AutoModelForSeq2SeqLM, BitsAndBytesConfig,)
from huggingface_hub import login
warnings.filterwarnings("ignore", category=UserWarning)
from langchain.agents import AgentType, initialize_agent
#from langchain.chat_models import ChatOpenAI
from transformers import StoppingCriteria
from transformers import StoppingCriteriaList
from langchain.llms import HuggingFacePipeline
from langchain.schema import BaseOutputParser
from transformers import pipeline
from transformers import BitsAndBytesConfig
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer

from datetime import datetime
from langchain import PromptTemplate, LLMChain
from langchain.agents import Tool
from langchain.chains import LLMMathChain
# from langchain_nomic.embeddings import NomicEmbeddings
from deep_translator import GoogleTranslator,single_detection
import google.generativeai as palm


from semantic_router import Route
from semantic_router import RouteLayer
from semantic_router.encoders import OpenAIEncoder
from semantic_router.encoders import HuggingFaceEncoder
from datetime import datetime, timedelta
import mysql.connector
from pymongo import MongoClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

mongo_username = os.environ.get('MONGO_USERNAME', 'root') 
mongo_password = os.environ.get('MONGO_PASSWORD', 'example')
# mongo_hostname = os.environ.get('MONGO_HOSTNAME', 'mongodb') 
mongo_hostname = os.environ.get('MONGO_HOSTNAME', 'localhost')
mongo_uri = f"mongodb://{mongo_username}:{mongo_password}@{mongo_hostname}:27017/"

client = MongoClient(mongo_uri)
db = client['coke'] 
read_collection = db['mer_info'] 
write_collection = db['mer_write']









host = 'localhost'  
user = 'admin'     
password = 'pass'   
database = 'coke'  
connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
cursor = connection.cursor()




select_query = f'''SELECT * from mer_details where id=1;'''
cursor.execute(select_query)

result_rows = cursor.fetchall()

for row in result_rows:
    sql_response = ", ".join(f"{column} is {value}" for column, value in zip(cursor.column_names, row))
    print(sql_response)

# Close the cursor and connection
cursor.close()
connection.close()





os.environ['GOOGLE_API_KEY'] =  'AIzaSyD1p0v1sjPmwkPM17yEn-gM95YJ-y27OGo'

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

print("LLM Initialized....")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

url = "http://localhost:6333"

client = QdrantClient(
    url=url, prefer_grpc=False
)

db = Qdrant(client=client, embeddings=embeddings, collection_name="vector_db")

retriever = db.as_retriever(search_kwargs={"k":3})

## Adding the CrossEncoderReranker using langchain over here
model_embed = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-large")
compressor = CrossEncoderReranker(model=model_embed, top_n=3)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever
)


# llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key="AIzaSyCjyyhW36eS4Tkk6N2gITsBDOR6Q9kJeRI", temperature=0.1)
llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash-002")
# llm=Ollama(base_url="https://81ba-34-93-180-130.ngrok-free.app",model="gemma2:27b")



# useful when user asks time
time_route = Route(
    name="get_time",
    utterances=[
        "what time is it?",
        "what is the time",
        "can u tell me the time",
    ],
)


encoder =HuggingFaceEncoder(model_name="nomic-ai/nomic-embed-text-v1.5")


routes = [time_route]
rl = RouteLayer(encoder=encoder, routes=routes, llm=llm)




def get_time():
    now = datetime.now()
    return f"The current time is {now.strftime('%H:%M')}. Use this information in your response."


def semantic_layer(query: str):
    route = rl(query)
    if route.name == "get_time":
        query += f" (SYSTEM NOTE: {get_time()})" 

    else:
        pass
    return query



def write_ticket_to_mongo(ticket):
    write_collection.insert_one(ticket)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    query_param1 = request.query_params.get('phone')
    print("parameter1",query_param1)
    query_param2 = request.query_params.get('timestamp')
    print("parameter2",query_param2)
    return templates.TemplateResponse("index.html", {"request": request, "phone": query_param1,"timestamp": query_param2})



prompt_template = """
    I am here to help you with any hotel-related inquiries, such as room prices, facilities, services, or booking rooms.
    If you don't know the answer, just say you don't know and avoid guessing.

  
    Context2:

    <hs>
    {history}
    </hs>
"""
context_message = """
    Context: {context}
    Question: {question}

    Provide only a short and helpful answer below, focusing on hotel-related assistance.
    Helpful short and summarized answer:
"""




prompt_template=sql_response+prompt_template+ context_message 
    
print(prompt_template)


prompt = PromptTemplate(template=prompt_template, input_variables=['history','context', 'question'])


qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type='stuff',
    # retriever=retriever,
    retriever=compression_retriever,
    verbose=True,
    chain_type_kwargs={
        "verbose": True,
        "prompt": prompt,
        "memory": ConversationBufferMemory(
            memory_key="history",
            input_key="question"
            ),
    }
    )
@app.post("/get_response")
async def get_response(query: str = Form(...),phoneNumber: str = Form(...),timestamp: str = Form(...),selectedLanguage: str = Form(...)):    
    global sql_response
    
    translator = GoogleTranslator(source=f'{selectedLanguage}', target='en')
    print(selectedLanguage)
    query=translator.translate(query)





    # uncomment this line to use semantic router library
    # query=semantic_layer(query)
    
    print("qa_chain",qa)

    response = qa(query)

    print(qa.combine_documents_chain.memory)

    print(response['result'])
    final_answer=response['result']
    translator = GoogleTranslator(source='en', target=f'{selectedLanguage}')
    final_answer=translator.translate(final_answer)
    response['result'] = f'{final_answer}'

    conversation = {
        "query": query,
        "result": response['result']
    }
    ticket={
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Chatbot Conversation": json.dumps(conversation)

    }

    if response['result']=="":
        response['result']="Sorry, I can't help with that"

    csv_file_path = "Conversations/generated_responses.csv"
    with open(csv_file_path, mode='a', newline='') as file:        
        writer = csv.DictWriter(file, fieldnames=["Timestamp","Chatbot Conversation"])
        writer.writerow(ticket)

    write_ticket_to_mongo(ticket)


    print("Printing the response over here")
    print(response)
 
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000,debug=True)