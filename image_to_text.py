from dotenv import load_dotenv
import os
import google.generativeai as genai
import textwrap
import requests
import PIL.Image

#Code for OCR using 

def to_markdown(text):
    if text.strip():
        text = text.replace('•', '  *')
        text = text.replace('The medicine is ', '', 1)
        text = text.replace('.', '', 1)
        text = text.replace(' ', '', 1)
        return(text)
    else:
        return "No text generated from the input. Please try again"

load_dotenv('key.env') #loads environment variables from a file named key.env
api_ = os.getenv('API_KEY') 
api_k = api_.replace('<', '').replace('>', '') #CONVERTS KEY to correct form, incase it has <> around it

GOOGLE_API_KEY=api_k #Enter your API key here (Instead of the environement variable)
genai.configure(api_key=GOOGLE_API_KEY)

config = {
  'temperature': 1.0, #randomness of the generated text
  'top_k': 100, #number of top predictions to consider
  'top_p': 0.9, #the nucleus sampling temperature
  'max_output_tokens': 500 #maximum length of the generated text
}

def image_to_text(file_path):
    img = PIL.Image.open(file_path)
    model = genai.GenerativeModel(model_name="gemini-pro-vision",generation_config=config)
    try:
        response = model.generate_content(["Extract text", img], stream=True)
        response.resolve()

        if response.parts:
          text = response.text
          extracted_text=to_markdown(text)
          return extracted_text
        else:
            if hasattr(response, 'blocked') and response.blocked:
                print("Response was blocked due to safety concerns.")
            else:
                print("Response does not contain a valid Part, API was not able to extract")
    except ValueError as e:
        print("An error occurred:", e)
    
    return None