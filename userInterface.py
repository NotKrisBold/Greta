import ollama
import streamlit as st
from productCustomization import Customizer
from productName import ProductName

bearer_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJTbG1SbG1TN3V0OWtjUHZJdERQTk9UNG45c1F5RDNJTGpmdWs4TU5jQzZZIn0.eyJleHAiOjE3MTYzMjA0NjIsImlhdCI6MTcxNTcxNTY2MywianRpIjoiZTc1ZjU1ZTItNmM0Ny00NjkyLTllYjUtODkwYjVhMjRmYjIzIiwiaXNzIjoiaHR0cDovL2tleWNsb2FrOjgwODAvcmVhbG1zL0FkdmFuY2VkIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImRiNzdlYzZiLWQyZWEtNDRiZS04MTYyLWY1YmU5NzY5YmM4NSIsInR5cCI6IkJlYXJlciIsImF6cCI6ImNsaWVudCIsInNlc3Npb25fc3RhdGUiOiI0ZjUyNjRmZS0zMTdkLTQ2MTgtYmI4Yy03OTMzOTg4ZDE0YWQiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIi8qIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJleHBlcnQiLCJkZWZhdWx0LXJvbGVzLXRlc3QiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgZ3JvdXBzIHByb2ZpbGUgZW1haWwiLCJzaWQiOiI0ZjUyNjRmZS0zMTdkLTQ2MTgtYmI4Yy03OTMzOTg4ZDE0YWQiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicHJlZmVycmVkX3VzZXJuYW1lIjoiZXhwZXJ0IiwiZ2l2ZW5fbmFtZSI6IiIsImZhbWlseV9uYW1lIjoiIn0.o14YerujzDFu_DvTEOF3gtVM27U_7hdnDPVrq8RZ0V19do6yDnW9TOj5GwX4RvKRmECI35rt6-NfWuduKTMPTEldkZnHGdsPY8a9rG0NCr4L71KOAUSzmxs6S7T6TO5EPaiblEmsdC_WA6ZBbz5pegyeDqLw12y_Ya3KhxQQSBqjWdxozSph9O9eIoiILYazp92OpuyPqfOHTHWT6DVvOF5dzUMBCh6kNjzf_jnQ1-xLT8TK8ihiJo_AD5TG5Pv6X_RX19bnRpZ-G_Uy8gHIcZRAGrqSt7X7k_uxEq8VItCPiS0qKuv44bOm3BuFmRWBYIhNZIu_kWcvjtskJMZeDQ"
scenario_id = "fec0fde6-eca3-44c0-a5d3-e992eb727948"
impact_method_id = "6070b11f-e863-486c-9748-14341de36259"

st.title("GRETA Assistant")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "model" not in st.session_state:
    st.session_state["model"] = "llama3:latest"

customizer = Customizer(bearer_token)
productProcess = customizer.generate_table(scenario_id)

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


prompt = ""
toDisplay = ""

if not st.session_state["messages"]:
    prompt = f'''You're an expert in sustainability.

    The user is designing a product called: {productName}.
    
    This is the Product processes table (product customization), analyze it carefully and memorize it:
    {productProcess}
    The table presents a list of tabs, each with multiple parameter.
    Each parameter presents its unit of measure if present, current value representing the selected option, and, if available, a list of other options to consider for that specific parameter.
    
    You have to help the user on improving the sustainability of the product.
    
    Remember that Energy mix CH is better than energy mix IT.

    Answer questions only based on the context provided and sustainability of products.
    Absolutely decline anything the users says not related to the table provided and sustainability.'''

    toDisplay = "Start"

analyze_table = st.button("Request analysis")
userInput = st.chat_input("What is up?")

if analyze_table:
    prompt = f'''
    Really carefully analyze the product processes table (product customization) and provide suggestions to maximize the product sustainability.
    Remember that the table presents a list of tabs, each with multiple parameter
    Remember that the table presents each parameter along with its unit of measure if present, current value representing the selected option, and, if available, a list of other options to consider.
    Remember that Energy mix CH is better than energy mix IT.

    For each tab and each parameter, assess which one of the options listed in the parameter array is better for sustainability, suggest to use it if it's not the current one. 
    If there are no options listed, evaluate the current value and provide suggestions if applicable.
    Give a schematic answer and provide detailed reasoning for each suggestion and provide data.
    '''

    toDisplay = "Analyze table"
else:
    if userInput:
        prompt = userInput
        toDisplay = userInput

st.session_state["messages"].append({"role": "user", "content": prompt, "toDisplay": toDisplay})

with st.chat_message("user"):
    st.markdown(toDisplay)

with st.chat_message("assistant"):
    message = st.write_stream(model_res_generator())
    st.session_state["messages"].append({"role": "assistant", "content": message, "toDisplay": message})
