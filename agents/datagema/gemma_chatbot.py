import torch
import data_gemma as dg
from google.colab import userdata
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import textwrap
from IPython.display import Markdown
import gradio as gr

# Fetch user tokens
DC_API_KEY = userdata.get('DC_API_KEY')
dc = dg.DataCommons(api_key=DC_API_KEY)

HF_TOKEN = userdata.get('HF_TOKEN')
HF_TOKEN = HF_TOKEN.strip().replace('\r', '').replace('\n', '')

# Configuration for model quantization
nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# Load the model and tokenizer
model_name = 'google/datagemma-rig-27b-it'
tokenizer = AutoTokenizer.from_pretrained(model_name, token=HF_TOKEN)
datagemma_model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    quantization_config=nf4_config,
    torch_dtype=torch.bfloat16,
    token=HF_TOKEN
)

# Wrap the model for use in RIGFlow
datagemma_model_wrapper = dg.HFBasic(datagemma_model, tokenizer)

# Function for displaying responses
def display_chat(prompt, text):
    formatted_prompt = "<font size='+1' color='brown'>🙋‍♂️<blockquote>" + prompt + "</blockquote></font>"
    text = text.replace('•', '  *')
    text = textwrap.indent(text, '> ', predicate=lambda _: True)
    formatted_text = "<font size='+1' color='teal'>🤖\n\n" + text + "\n</font>"
    return Markdown(formatted_prompt + formatted_text)

# Gradio interface function
def chatbot(query):
    try:
        ans = dg.RIGFlow(
            llm=datagemma_model_wrapper,
            data_fetcher=dc,
            verbose=False
        ).query(query=query)
        return ans.answer()
    except Exception as e:
        return f"Error: {str(e)}"

# Create the Gradio interface
interface = gr.Interface(
    fn=chatbot,
    inputs=gr.Textbox(label="Enter your query"),
    outputs=gr.Textbox(label="Response"),
    title="Gemma Chatbot",
    description="Ask any question related to demographics, health, education, and more!"
)

# Launch the interface
interface.launch(share=True)
