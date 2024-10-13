from datetime import datetime

import streamlit as st
from pathlib import Path
import json
from Parsers.response_parser import ResponseParser
import re
from config import OPENAI_API_KEY, ROOT_PATH
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


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css(Path(ROOT_PATH, 'src/css/style.css'))

# Sidebar with logo
st.sidebar.image("src/logo.png", use_column_width=True)
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
st.write('<p class="title-subtext">Generate marketing strategies for different platforms (Instagram, LinkedIn, Email) based on product details.</p><hr>', unsafe_allow_html=True)

# Input fields for product details
col1, col2 = st.columns(2)

with col1:
    product_name = st.text_input("Product Name", "TexSneaks", placeholder="Product Name")
    st.write('<p class="input-example">Eg. TexSneaks</p>', unsafe_allow_html=True)

    product_category = st.text_input("Product Category", "Shoes", placeholder="Product Category")
    st.write('<p class="input-example">Eg. Shoes</p>', unsafe_allow_html=True)

    product_stage = st.selectbox("Product Stage", ["Launch", "Growth", "Maturity", "Decline"], index=0)
    st.write('<p class="input-example">Choose an option</p>', unsafe_allow_html=True)

with col2:
    product_description = st.text_area("Product Description",
                                "TexSneaks offers trendy, high-quality, and eye-catching sneakers that are perfect for fashion-forward teenagers.",
                                height=290)
    
target_audience = st.text_area("Target Audience", "Teenagers aged 13-19, fashion-conscious, interested in streetwear.")

col3, col4 = st.columns(2)

with col3:
    region = st.text_input("Region", "Texas")
    st.write('<p class="input-example">Eg. Texas</p>', unsafe_allow_html=True)

    product_pricing = st.text_input("Product Pricing", "Mid-range to high-end")
    st.write('<p class="input-example">Eg. Mid-range to high-end</p>', unsafe_allow_html=True)

with col4:
    marketing_goals = st.text_input("Marketing Goals", "Increase brand awareness and sales.")
    st.write('<p class="input-example">Eg. Increase brand awareness and sales</p>', unsafe_allow_html=True)

    budget_range = st.text_input("Budget Range", "1000-5000")
    st.write('<p class="input-example">Eg. 1000-5000</p>', unsafe_allow_html=True)

unique_selling_point = st.text_input("Unique Selling Point", "Trendy and customizable designs.")
st.write('<p class="input-example">Eg. Trendy and customizable designs</p><hr>', unsafe_allow_html=True)

st.write("### Persona Details")

# Input fields for product details
col6, col7 = st.columns(2)

with col6:
    persona_gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=0)
    st.write('<p class="input-example">Eg. Male</p>', unsafe_allow_html=True)

with col7:
    persona_country = st.text_input("Country", "USA")
    st.write('<p class="input-example">Eg. USA</p>', unsafe_allow_html=True)
    
persona_age = st.text_input("Age", "25")
st.write('<p class="input-example">Eg. 25</p>', unsafe_allow_html=True)

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

st.write('<p class="multiselect-pretext">Select all the actions you want to include:</p>', unsafe_allow_html=True)
action_choice = st.selectbox(
    "Choose the action:",
    options=["Generate Marketing Strategies", "Generate User Persona"]
)

available_prompts = {
    'LinkedIn Post': "linkedin_post_creation_prompt",
    'Instagram Post': "instagram_post_creation_prompt",
    'Email Template': "email_template_prompt",
    'Channel Guidance': "channel_investment_guidance_prompt",
    'Detailed Strategy Development': "detailed_stategy_development_prompt",
    'Digital Post': "digital_marketing_focus_prompt"
}

# Checkbox to select prompts
selected_prompts = st.multiselect(
    "Choose the marketing strategies to generate:",
    options=["LinkedIn Post", "Instagram Post", "Email Template",
            "Channel Investment Guidance", "Detailed Strategy Development",
            "Digital Marketing Focus"],
    default=["LinkedIn Post", "Instagram Post", "Email Template"]
)
st.write('<hr class="btn-separator">', unsafe_allow_html=True)

# Generate button
_, col8, _ = st.columns(3)
if col8.button("Generate Analysis"):
    if action_choice == "Generate Marketing Strategies":
        if not selected_prompts:
            selected_prompts = available_prompts.values()
        else:
            selected_prompts = [available_prompts[prompt] for prompt in selected_prompts]

        results = generate_strategy(product_name, product_description, product_category, product_stage,
                                    target_audience, region, product_pricing, unique_selling_point,
                                    marketing_goals, budget_range, selected_prompts, persona_attributes)

        st.session_state['generated_history'].append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'content': results
        })

        st.write('<p class="output-title">Generated Marketing Strategies:</p>', unsafe_allow_html=True)
        for prompt, result in results.items():
            result = re.sub(r'[\x00-\x1F\x7F]', '', result)

            # Remove leading/trailing tags
            json_part = re.search(r'\{.*\}', result)
            if json_part:
                result = json_part.group(0)

            with st.expander(f"Click to Expand/Collapse details for {prompt.replace('_', ' ').title()}", expanded=False):
                st.subheader(f"Strategy for {prompt.replace('_', ' ').title()}:")
                parsed_result = eval(result)  # Assuming result is a JSON-like string

                # Display each part of the response in a structured manner
                if 'action' in parsed_result:
                    st.write(f'<span class="highlight-text">Action</span>: {parsed_result['action']}', unsafe_allow_html=True)
                if 'response' in parsed_result:
                    st.write(f'<span class="highlight-text">Response</span>: {parsed_result['response']}', unsafe_allow_html=True)
            
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

        try:
            persona_result = json.loads(persona_result)  # Convert string to dictionary
        except json.JSONDecodeError:
            st.error("Error parsing the persona result. Please ensure it's in valid JSON format.")
            persona_result = {}

        # Append to session history if the result is valid
        if persona_result:
            st.session_state['generated_history'].append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'content': persona_result
            })

            # Display persona result
            st.write("## Generated User Persona:")
            st.write(persona_result)

            # Emojis for different sections
            emojis = ["✅", "🤔", "🎯", "🚀", "💡", "🔖"]

            # Iterate over the persona result and display with corresponding emojis
            for i, (key, value) in enumerate(persona_result.items()):
                if key != "Other options":  # Assuming you may have other options later
                    st.write(f"{emojis[i]} **{key}**:")
                    with st.expander(f"View details for {key}", expanded=False):
                        st.write(value)
                else:
                    # Handle "Other options" if needed
                    st.write(f"{emojis[-1]} **{key}**:")
                    st.write(persona_result[key])

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