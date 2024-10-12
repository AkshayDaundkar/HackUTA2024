# llm.py
import openai
from config import OPENAI_API_KEY
from src.Prompts.prompts import post_creation_prompt

openai.api_key = OPENAI_API_KEY

def generate_strategy(product_name, product_description, product_category, product_stage, target_audience, region, product_pricing):
    final_prompt = post_creation_prompt.format(
        Product_Name=product_name,
        Product_Description=product_description,
        Product_Category=product_category,
        Product_Stage=product_stage,
        Audience=target_audience,
        Region=region,
        Pricing=product_pricing
    )

    messages = [
        {"role": "system", "content":final_prompt},
        {"role": "user", "content": "help me generate a Instagram Post for my Product"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=1500
    )

    # Return the response content
    return response['choices'][0]['message']['content']
