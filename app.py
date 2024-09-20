# app.py

import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai==0.27.0

# Set up your OpenAI API key
openai.api_key = st.secrets["sk-l3xuEH2Dbo6TjzgmaxgTAiSwa5Tea-1ss66c3ApOd0T3BlbkFJnfCZCzmDYIRH4I6YO9377TwPkmmOS_E111OL3vSy4A"]

st.title("Logical Fallacy and Cognitive Bias Detector")

# Input options
option = st.selectbox(
    'Choose input method:',
    ('Enter URL', 'Paste Text')
)

text = ""

if option == 'Enter URL':
    url = st.text_input('Enter the URL of the web page:')
    if url:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract text from paragraphs
            paragraphs = soup.find_all('p')
            text = ' '.join([para.get_text() for para in paragraphs])
        except Exception as e:
            st.error(f"Error fetching the URL: {e}")
else:
    text = st.text_area('Paste the text content here:')

if text:
    if st.button('Analyze'):
        with st.spinner('Analyzing...'):
            try:
                # Prepare the prompt for OpenAI
                prompt = f"Identify and list any logical fallacies and cognitive biases present in the following text:\n\n{text}\n\nFor each identified instance, provide the name of the fallacy or bias and a brief explanation."

                # Call the OpenAI API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert in logical reasoning and cognitive psychology."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )

                analysis = response['choices'][0]['message']['content']
                st.success('Analysis complete!')
                st.write(analysis)
            except Exception as e:
                st.error(f"Error during analysis: {e}")
