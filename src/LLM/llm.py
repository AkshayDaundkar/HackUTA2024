# llm.py
from langchain_community.llms.openai import OpenAI
from src.Prompts.prompts import post_creation_prompt
from config import OPENAI_API_KEY
import openai
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

openai.api_key = OPENAI_API_KEY

class LLM:
    def __init__(self, db):
        self.db = db

def generate_strategy(product_name, product_description, product_category, product_stage, target_audience, region,
                      product_pricing,unique_selling_point,marketing_goals,budget_range):
    # test_prompt = db.get_prompt_data()
    test_prompt=post_creation_prompt
    # print(test_prompt)

    final_prompt = test_prompt.format(
        Product_Name=product_name,
        Product_Description=product_description,
        Product_Category=product_category,
        Product_Stage=product_stage,
        Audience=target_audience,
        Region=region,
        Pricing=product_pricing,
        Unique_Selling_Points = unique_selling_point,
        Marketing_Goals = marketing_goals,
        Budget_Range = budget_range
    )

    messages = [
        {"role": "system", "content": final_prompt},
        {"role": "user", "content": "help me generate a Channel Investment Guidelines for my Product"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=1500
    )

    # Return the response content
    return response['choices'][0]['message']['content']
