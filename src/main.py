import streamlit as st
from LLM.llm import LLM
from Parsers.response_parser import ResponseParser
import re

from config import OPENAI_API_KEY
from database import MongoDBData
import openai
from dotenv import load_dotenv

from Prompts.promptss import *

load_dotenv()  # take environment variables from .env

openai.api_key = OPENAI_API_KEY
db = MongoDBData('prompt_db', 'input_prompt')


def generate_strategy(product_name, product_description, product_category, product_stage, target_audience, region,
                      product_pricing,unique_selling_point,marketing_goals,budget_range):
    # test_prompt = db.get_prompt_data()
    test_prompt=linkedin_post_creation_prompt

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

    print("final prommpt:", final_prompt)

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




# Streamlit app title and description
st.title("Marketing Strategy Generator")
st.write("Generate marketing strategies for different platforms (Instagram, LinkedIn, Email) based on product details.")

# Input fields for product details
product_name = st.text_input("Product Name", "TexSneaks")
product_description = st.text_area("Product Description", "TexSneaks offers trendy, high-quality, and eye-catching sneakers that are perfect for fashion-forward teenagers.")
product_category = st.text_input("Product Category", "Shoes")
product_stage = st.selectbox("Product Stage", ["Launch", "Growth", "Maturity", "Decline"], index=0)
target_audience = st.text_area("Target Audience", "Teenagers aged 13-19, fashion-conscious, interested in streetwear.")
region = st.text_input("Region", "Texas")
product_pricing = st.text_input("Product Pricing", "Mid-range to high-end")
unique_selling_point = st.text_input("Unique Selling Point", "Trendy and customizable designs.")
marketing_goals = st.text_input("Marketing Goals", "Increase brand awareness and sales.")
budget_range = st.text_input("Budget Range", "1000-5000")

# Button to generate the marketing strategy
if st.button("Generate Marketing Strategy"):
    # Call the strategy generation function
    result = generate_strategy(
        product_name,
        product_description,
        product_category,
        product_stage,
        target_audience,
        region,
        product_pricing,
        unique_selling_point,
        marketing_goals,
        budget_range
    )

    # Clean the result to avoid control characters
    result = re.sub(r'[\x00-\x1F\x7F]', '', result)

    # Parse the result using ResponseParser
    parser = ResponseParser(result)
    parsed_instagram = parser.parse_instagram_post()
    parsed_linkedin = parser.parse_linkedin_post()
    parsed_email = parser.parse_email_template()

    # Display the generated marketing strategies
    st.write("## Generated Marketing Strategy:")

    if parsed_instagram:
        st.subheader("Instagram Post:")
        st.write(f"**Action**: {parsed_instagram['action']}")
        st.write(parsed_instagram['content'])

    if parsed_linkedin:
        st.subheader("LinkedIn Post:")
        st.write(f"**Action**: {parsed_linkedin['action']}")
        st.write(parsed_linkedin['content'])

    if parsed_email:
        st.subheader("Email Template:")
        st.write(f"**Action**: {parsed_email['action']}")
        st.write(parsed_email['content'])

