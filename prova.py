import ollama
import streamlit as st
from calculatedScenario import Calculator
from productCustomization import Customizer

bearer_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJTbG1SbG1TN3V0OWtjUHZJdERQTk9UNG45c1F5RDNJTGpmdWs4TU5jQzZZIn0.eyJleHAiOjE3MTM4NTk1MzgsImlhdCI6MTcxMzI1NDczOCwianRpIjoiODcwZTIzMzUtYzNiOC00MmYyLThjYmItNTYyODhlN2RjZTUwIiwiaXNzIjoiaHR0cDovL2tleWNsb2FrOjgwODAvcmVhbG1zL0FkdmFuY2VkIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImRiNzdlYzZiLWQyZWEtNDRiZS04MTYyLWY1YmU5NzY5YmM4NSIsInR5cCI6IkJlYXJlciIsImF6cCI6ImNsaWVudCIsInNlc3Npb25fc3RhdGUiOiJkNmMyOGMzNC1jNzNiLTRkMDMtYjM5OC00MmM2YjdkOWY1NzAiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIi8qIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJleHBlcnQiLCJkZWZhdWx0LXJvbGVzLXRlc3QiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgZ3JvdXBzIHByb2ZpbGUgZW1haWwiLCJzaWQiOiJkNmMyOGMzNC1jNzNiLTRkMDMtYjM5OC00MmM2YjdkOWY1NzAiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicHJlZmVycmVkX3VzZXJuYW1lIjoiZXhwZXJ0IiwiZ2l2ZW5fbmFtZSI6IiIsImZhbWlseV9uYW1lIjoiIn0.qhuXmSWU3vgZOX4PI3-uJVa_0CnE_P3bs5u88XM6BtWYguSTW4FF508VG___rEZBBqAXPp4JDmN-wW1I-tWMqK7brmG2b8t1bSPpZ04T47qJ-VQwLd6rOoZ72gzMZ2Nf9SQYWV7TgzIlITST0rUT94Yc9_Z2x56nvA43Ifgcr6goF4wa8UkWaqdtk0imYV7cNnGA0SQ6-zbXi6rEUISo9AZpLcV3Z84DvKqJ1H_XWDWvzUsvqunJYePMAskMpszu1SnIMPIoshxpRNw15FagePgXNS55eHJ53O4j7NFzc0Rd-Ky3dKIpEnvDcxiY3ltbUw6sht2wYJfMW9A1WYLmBw"
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
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message = st.write_stream(model_res_generator())
        st.session_state["messages"].append({"role": "assistant", "content": message})
