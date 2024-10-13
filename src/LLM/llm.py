# llm.py
from langchain_community.llms.openai import OpenAI

from config import OPENAI_API_KEY
from src.database import MongoDBData
import openai
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

openai.api_key = OPENAI_API_KEY
db = MongoDBData('prompt_db', 'input_prompt')


def generate_strategy(product_name, product_description, product_category, product_stage, target_audience, region,
                      product_pricing):
    test_prompt = db.get_prompt_data()
    # print(test_prompt)

    final_prompt = test_prompt.format(
        Product_Name=product_name,
        Product_Description=product_description,
        Product_Category=product_category,
        Product_Stage=product_stage,
        Audience=target_audience,
        Region=region,
        Pricing=product_pricing
    )

    messages = [
        {"role": "system", "content": final_prompt},
        {"role": "user", "content": "help me generate a Instagram Post for my Product"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=1500
    )

    # Return the response content
    return response['choices'][0]['message']['content']
