import streamlit as st
import requests 
from app.config.settings import settings 
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
logger = get_logger(__name__)
st.set_page_config(page_title="Multi AI Agent Chat",layout="centered",page_icon="🤖")
st.title("🤖 Multi AI Agent Chat Interface ")

system_prompt=st.text_area("define your Ai agent: ",height=70)
selected_model=st.selectbox("Select AI Model:",options=settings.ALLOWED_MODEL_NAMES)
allow_web_search=st.checkbox("Allow Web Search",value=False)
user_query=st.text_area("Enter your query:",height=150)
API_URL="http://127.0.0.1:9999/"
if st.button("Ask agent") and user_query.strip():
    with st.spinner("Getting response from AI agent..."):
        try:
            payload={
                "model_name":selected_model,
                "system_prompt":system_prompt,
                "messages":[user_query],
                "allow_search":allow_web_search
            }
            response=requests.post(API_URL,json=payload)
            if response.status_code==200:
                agent_response=response.json().get("response","")
                st.success("Response from AI Agent:")
                st.markdown(agent_response.replace("\n","<br>"),unsafe_allow_html=True)
            else:
                logger.error(f"API returned error {response.status_code}: {response.text}")
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            logger.error(f"Exception during API call: {e}")
            st.error(f"An error occurred: {str(CustomException('Failed to get response from AI agent',e))}")