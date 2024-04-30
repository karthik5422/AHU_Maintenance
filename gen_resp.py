import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.environ["GEMINI_API_KEY"]

# Initialize GenerativeAI model
model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7, google_api_key=api_key)

# safety_settings = [
#   {
#     "category": "HARM_CATEGORY_HARASSMENT",
#     "threshold": "BLOCK_NONE"
#   },
#   {
#     "category": "HARM_CATEGORY_HATE_SPEECH",
#     "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#   },
#   {
#     "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
#     "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#   },
#   {
#     "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
#     "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#   }
# ]

# Prompt template to query GenerativeAI
prompt1 = ChatPromptTemplate.from_template("""
As an assistant, your role is to analyze data from an air handling unit (AHU) and provide insights based on its performance.
Your responsibility includes interpreting the given AHU data and offering answers or recommendations accordingly.

The AHU dataset comprises the following columns:
Date, fan_status, filter_status, uv_lamp_status, uv_lamp_hours, sa_temp, sa_set_temp, chw_inlet_temp, chw_outlet_temp, chw_delta_temp, ra_co2, ra_temp, ahu_perf.

- If 'ahu_perf' is labeled as "Normal," it indicates no maintenance is required.
- If 'ahu_perf' other than "Normal" i.e., "Low" is low maintenance is required, "Medium" is medium maintenance is required, "High" is high maintenance is required and for "critical" denotes few part replacements and calibration are needed.

When responding to questions, consider both the column names and the provided data for accurate answers. 
Utilize your knowledge base to provide insightful responses beyond the given data.

Here are the 5 consecutive data points along with the column names:
{data_preview}

Question: {question}
Context: {context}

Answer:""")

output_parser = StrOutputParser()

chain1 = prompt1 | model | output_parser


context = """We are analyzing the AHU data for the past week to identify any potential maintenance issues or deviations from normal operation. The data was collected from sensors installed in the HVAC system, and we are particularly interested in understanding the performance during peak occupancy hours."""

def generate_response(data):
    try:
       # Generate response
        response = chain1.invoke({"context": context, "question": "what are the actions to be perform to avoid downtime of AHU", "data_preview": data})
    except:
        response = "Sorry, I couldn't generate a response."
    return response


prompt2 = ChatPromptTemplate.from_template("{question}")

chain2 = prompt2 | model | output_parser



def common_response(question):
    try:
       # Generate response
        response = chain2.invoke({"question": question})
    except:
        response = "Sorry, I couldn't generate a response."
    return response
