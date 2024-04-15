import ollama
import streamlit as st
from calculatedScenario import Calculator
from productCustomization import Customizer

bearer_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJTbG1SbG1TN3V0OWtjUHZJdERQTk9UNG45c1F5RDNJTGpmdWs4TU5jQzZZIn0.eyJleHAiOjE3MTM2MjU1OTUsImlhdCI6MTcxMzAyMDgwNSwianRpIjoiMGUyNTZlZTItZGQwNy00YTcwLWI1ZGItYzdiNmQxZDQxMjg4IiwiaXNzIjoiaHR0cDovL2tleWNsb2FrOjgwODAvcmVhbG1zL0FkdmFuY2VkIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImRiNzdlYzZiLWQyZWEtNDRiZS04MTYyLWY1YmU5NzY5YmM4NSIsInR5cCI6IkJlYXJlciIsImF6cCI6ImNsaWVudCIsInNlc3Npb25fc3RhdGUiOiJmZWU5YWNjNS05NGExLTRmNzEtOTk2Yy04NDU4YWZhMGZjM2YiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIi8qIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJleHBlcnQiLCJkZWZhdWx0LXJvbGVzLXRlc3QiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgZ3JvdXBzIHByb2ZpbGUgZW1haWwiLCJzaWQiOiJmZWU5YWNjNS05NGExLTRmNzEtOTk2Yy04NDU4YWZhMGZjM2YiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicHJlZmVycmVkX3VzZXJuYW1lIjoiZXhwZXJ0IiwiZ2l2ZW5fbmFtZSI6IiIsImZhbWlseV9uYW1lIjoiIn0.XVTR2GfQ7bmcE5XJ550szjXrjY5DkNlPKNWzl4ITe25hbcFm37qPNXYZWTGD2umx8gdWkRUMbI6i0XrNPDSKy-hAYe_DRA9uLPplmRva9gSxkfjHr5cRRHf0YZ7pCRpNpNuVl6rU80VXLPxPeLXfw2SR4IZYHxpEcPyEPHikcMWz5V4oMnLDr7w6UIuxMPO_WaHQl3GF20FoY9dMFrFGGSbwhE86mWXZG3MfqAmua-It1h1S8FMFrb8aVA57o7Fp0tlqMzXU5mFMOmNTidt6c-FMIufHJAi0NimrwdDn5egIYtv7vbcwTHsD7vJl4kMnZXyaBW8lUa6z9WFu_Spv5g"
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

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def model_res_generator():
    stream = ollama.chat(
        model=st.session_state["model"],
        messages=st.session_state["messages"],
        stream=True
    )
    for chunk in stream:
        yield chunk["message"]["content"]


if prompt := st.chat_input("What is up?"):
    newPrompt = f'''Answer the following question based on the provided context only. 

    <context>
    Product Processes Table (includes current values and alternative options):
    {productProcess.to_json()}

    LCA Table (provides Life Cycle Assessment data of the product):
    {lca.to_json()}
    </context>

    Question: {prompt}'''

    # add latest message to history in format {role, content}
    st.session_state["messages"].append({"role": "user", "content": newPrompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message = st.write_stream(model_res_generator())
        st.session_state["messages"].append({"role": "assistant", "content": message})
