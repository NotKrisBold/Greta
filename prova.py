import ollama
import streamlit as st
from calculatedScenario import Calculator
from productCustomization import Customizer
from productName import ProductName

bearer_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJTbG1SbG1TN3V0OWtjUHZJdERQTk9UNG45c1F5RDNJTGpmdWs4TU5jQzZZIn0.eyJleHAiOjE3MTQ0NzQ1MjUsImlhdCI6MTcxMzg2OTcyNSwianRpIjoiYTQwODYxM2EtY2I3ZC00YTNlLWI2OTMtNDAxMTBjOGJhYWRiIiwiaXNzIjoiaHR0cDovL2tleWNsb2FrOjgwODAvcmVhbG1zL0FkdmFuY2VkIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImRiNzdlYzZiLWQyZWEtNDRiZS04MTYyLWY1YmU5NzY5YmM4NSIsInR5cCI6IkJlYXJlciIsImF6cCI6ImNsaWVudCIsInNlc3Npb25fc3RhdGUiOiJhYzc5MjA0Zi0yNjYyLTRkMzEtODlmOC1lYTBlNGY1YjQ5OGIiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIi8qIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJleHBlcnQiLCJkZWZhdWx0LXJvbGVzLXRlc3QiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgZ3JvdXBzIHByb2ZpbGUgZW1haWwiLCJzaWQiOiJhYzc5MjA0Zi0yNjYyLTRkMzEtODlmOC1lYTBlNGY1YjQ5OGIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicHJlZmVycmVkX3VzZXJuYW1lIjoiZXhwZXJ0IiwiZ2l2ZW5fbmFtZSI6IiIsImZhbWlseV9uYW1lIjoiIn0.ClD-_hlV0cX2U-vERjiv6Nnv3N29Jn3tptgAN-SxYZEnhYNWGv8jILYWrf2E3QGWBvREY8uLvMv_3XvKgdQN3WpDD_bYKc6mgt3groPlwAK9aEjvDJ0G0rC-U2drJ4vsBYg7E3kd_3buAFBqA0gkFH_ZiLYsoIiJNrU2jPbBrOC6MT4Y6CZeNTzndpsxj-Iposi7uLwngXQgVkKBq3wg25J2Y5lUYdnw2hffObRlh_eMjCQIolw73AuFB-_SngIkk6ZJQu2GclHRFLbAG8G0DURxeFldIG5r8VtMj1V3mlUtsD2uOvAQC-jibBE4maWAmfXVlZUSw6tWZ8CD2Ansmw"
scenario_id = "fec0fde6-eca3-44c0-a5d3-e992eb727948"
impact_method_id = "6070b11f-e863-486c-9748-14341de36259"

st.title("Ollama Python Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "model" not in st.session_state:
    st.session_state["model"] = ""

models = [model["name"] for model in ollama.list()["models"]]
st.session_state["model"] = st.selectbox("Choose your model", models)

customizer = Customizer(bearer_token)
productProcess = customizer.generate_table(scenario_id)

calculator = Calculator(bearer_token)
lca = calculator.generate_table(scenario_id, impact_method_id)

productName = ProductName(bearer_token).get_name(scenario_id)

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["toDisplay"])


def model_res_generator():
    stream = ollama.chat(
        model=st.session_state["model"],
        messages=st.session_state["messages"],
        stream=True
    )
    for chunk in stream:
        yield chunk["message"]["content"]


if not st.session_state["messages"]:
    prompt = f''''You are an expert in sustainability.
            <context>
            The user is designing a product called: {productName}.
            This is the processes table of the product, analyze it carefully and memorize it:
            {productProcess}    
            <context>

            Answer questions only based on the context provided and sustainability of products.
            Absolutely decline anything the users says not related to the context and sustainability'''

    st.session_state["messages"].append({"role": "user", "content": prompt, "toDisplay": ""})
    with st.chat_message("assistant"):
        message = st.write_stream(model_res_generator())
        st.session_state["messages"].append({"role": "assistant", "content": message, "toDisplay": ""})

analyze_table = st.button("Analyze table")
userInput = st.chat_input("What is up?")

if analyze_table:
    prompt = f'''
    Analyze the product processes table and provide suggestions to maximize the product sustainability.

    For each tab and each parameter, assess which one of the options listed in the parameter array is better for sustainability, suggest to use it if it's not the current one. 
    If there are no options listed, evaluate the current value and provide suggestions if applicable.
    Give a schematic answer and provide detailed reasoning for each suggestion and provide data.
    '''

    st.session_state["messages"].append({"role": "user", "content": prompt, "toDisplay": "Analyze table"})

    with st.chat_message("assistant"):
        message = st.write_stream(model_res_generator())
        st.session_state["messages"].append({"role": "assistant", "content": message, "toDisplay": message})

else:
    if userInput:
        prompt = userInput

        st.session_state["messages"].append({"role": "user", "content": prompt, "toDisplay": prompt})

        with st.chat_message("user"):
            st.markdown(userInput)

        with st.chat_message("assistant"):
            message = st.write_stream(model_res_generator())
            st.session_state["messages"].append({"role": "assistant", "content": message, "toDisplay": message})
