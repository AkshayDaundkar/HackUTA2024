from datetime import datetime

import streamlit as st

from Parsers.response_parser import ResponseParser
import re
from config import OPENAI_API_KEY
from database import MongoDBData
import openai
from dotenv import load_dotenv
from Prompts.promptss import linkedin_post_creation_prompt, instagram_post_creation_prompt, email_template_prompt, \
    channel_investment_guidance_prompt, detailed_stategy_development_prompt, digital_marketing_focus_prompt, \
    generate_user_persona

load_dotenv()  # Load environment variables
openai.api_key = OPENAI_API_KEY
# db = MongoDBData('prompt_db', 'input_prompt')


if 'generated_history' not in st.session_state:
    st.session_state['generated_history'] = []  # List to store previous responses

# Function to generate marketing strategies
def generate_strategy(product_name, product_description, product_category, product_stage, target_audience, region,
                      product_pricing, unique_selling_point, marketing_goals, budget_range, prompts,persona_attributes):
    results = {}

    for prompt in prompts:

        if prompt=="linkedin_post_creation_prompt":
            test_prompt=linkedin_post_creation_prompt
        elif prompt=="instagram_post_creation_prompt":
            test_prompt=instagram_post_creation_prompt
        elif prompt=="email_template_prompt":
            test_prompt=email_template_prompt
        elif prompt=="channel_investment_guidance_prompt":
            test_prompt=channel_investment_guidance_prompt
        elif prompt=="detailed_stategy_development_prompt":
            test_prompt=detailed_stategy_development_prompt
        elif prompt=="digital_marketing_focus_prompt":
            test_prompt = digital_marketing_focus_prompt
        else:
            test_prompt = generate_user_persona

        final_prompt = test_prompt.format(
            Product_Name=product_name,
            Product_Description=product_description,
            Product_Category=product_category,
            Product_Stage=product_stage,
            Audience=target_audience,
            Region=region,
            Pricing=product_pricing,
            Unique_Selling_Points=unique_selling_point,
            Marketing_Goals=marketing_goals,
            Budget_Range=budget_range
        )
        # print("final prommpt:",final_prompt)

        messages = [

            {"role": "system", "content": final_prompt},
            {"role": "user", "content": "help me generate a marketing output for my Product"}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=1500
        )

        # Clean and store the result
        results[prompt] = re.sub(r'[\x00-\x1F\x7F]', '', response['choices'][0]['message']['content'])
    return results



st.markdown(
    """
    <style>
    h1 {
        color: #b7c439; /* Tomato */
        text-align: center;
    }
    h2 {
        color: #b7c439; /* SteelBlue */
        text-align: center;
    }
    h3 {
        color: #b7c439; /* SeaGreen */
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True
)

# Sidebar with logo
st.sidebar.image("logo.png", use_column_width=True)
st.sidebar.title("Marketing Strategy Generator")

# History sidebar
st.sidebar.subheader("History")
if st.session_state['generated_history']:
    for i, entry in enumerate(st.session_state['generated_history']):
        if st.sidebar.button(f"Result {i + 1} - {entry['timestamp']}"):
            st.write("## Previous Generated Results")
            st.write(entry['content'])
else:
    st.sidebar.write("No history yet.")

# Streamlit app title and description
st.title("Marketing Strategy Generator")
st.write("Generate marketing strategies for different platforms (Instagram, LinkedIn, Email) based on product details.")

# Input fields for product details
product_name = st.text_input("Product Name", "TexSneaks")
product_description = st.text_area("Product Description",
                                   "TexSneaks offers trendy, high-quality, and eye-catching sneakers that are perfect for fashion-forward teenagers.")
product_category = st.text_input("Product Category", "Shoes")
product_stage = st.selectbox("Product Stage", ["Launch", "Growth", "Maturity", "Decline"], index=0)
target_audience = st.text_area("Target Audience", "Teenagers aged 13-19, fashion-conscious, interested in streetwear.")
region = st.text_input("Region", "Texas")
product_pricing = st.text_input("Product Pricing", "Mid-range to high-end")
unique_selling_point = st.text_input("Unique Selling Point", "Trendy and customizable designs.")
marketing_goals = st.text_input("Marketing Goals", "Increase brand awareness and sales.")
budget_range = st.text_input("Budget Range", "1000-5000")


st.write("### Persona Details")
persona_gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=0)
persona_country = st.text_input("Country", "USA")
persona_age = st.text_input("Age", "25")
persona_comments = st.text_area("Additional Comments", "The persona is tech-savvy and highly engaged on social media.")

# Combine persona attributes into a dictionary
persona_attributes = {
    "gender": persona_gender,
    "country": persona_country,
    "age": persona_age,
    "comments": persona_comments,
    "product_category":product_category,
    "product_description":product_description
}

st.write("### Select the action you want to include:")
action_choice = st.selectbox(
    "Choose the action:",
    options=["Generate Marketing Strategies", "Generate User Persona"]
)

# Checkbox to select prompts
st.write("Select the strategies you want to generate:")
selected_prompts = st.multiselect(
    "Choose the marketing strategies to generate:",
    options=["linkedin_post_creation_prompt", "instagram_post_creation_prompt", "email_template_prompt",
             "channel_investment_guidance_prompt", "detailed_stategy_development_prompt",
             "digital_marketing_focus_prompt"],
    default=["linkedin_post_creation_prompt", "instagram_post_creation_prompt", "email_template_prompt"]
)

# Generate button
if st.button("Generate"):
    if action_choice == "Generate Marketing Strategies":
        if not selected_prompts:
            selected_prompts = [
                "linkedin_post_creation_prompt",
                "instagram_post_creation_prompt",
                "email_template_prompt",
                "channel_investment_guidance_prompt",
                "detailed_stategy_development_prompt",
                "digital_marketing_focus_prompt"
            ]

        results = generate_strategy(product_name, product_description, product_category, product_stage,
                                    target_audience, region, product_pricing, unique_selling_point,
                                    marketing_goals, budget_range, selected_prompts, persona_attributes)

        st.session_state['generated_history'].append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'content': results
        })

        st.write("## Generated Marketing Strategies:")
        for prompt, result in results.items():
            result = re.sub(r'[\x00-\x1F\x7F]', '', result)

            # Remove leading/trailing tags
            json_part = re.search(r'\{.*\}', result)
            if json_part:
                result = json_part.group(0)

            st.subheader(f"Strategy for {prompt.replace('_', ' ').title()}:")
            parsed_result = eval(result)  # Assuming result is a JSON-like string

            # Display each part of the response
            if 'action' in parsed_result:
                st.write(f"**Action**: {parsed_result['action']}")
            if 'response' in parsed_result:
                st.write(parsed_result['response'])
            st.write("---")
            
        st.image("https://miro.medium.com/v2/resize:fit:1400/1*GugoFZUldUF6RncoKt_4Bw.png", caption="This is a AI generated image.",
                 use_column_width=True)


    elif action_choice == "Generate User Persona":
        # Generate persona using the selected persona attributes
        persona_prompt = generate_user_persona.format(**persona_attributes)

        messages = [
            {"role": "system", "content": persona_prompt},
            {"role": "user", "content": "Generate a user persona"}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=1500
        )

        persona_result = re.sub(r'[\x00-\x1F\x7F]', '', response['choices'][0]['message']['content'])
        st.session_state['generated_history'].append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'content': persona_result
        })

        st.write("## Generated User Persona:")
        st.write(persona_result)

st.markdown("""
    <style>
    footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #333;
        color: white;
        text-align: center;
        padding: 10px;
    }
    </style>

    <footer>
        <p>© 2024 MarketIQ - All Rights Reserved</p>
    </footer>
    """, unsafe_allow_html=True)