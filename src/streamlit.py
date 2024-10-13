import streamlit as st
from Parsers.response_parser import ResponseParser
import re
from config import OPENAI_API_KEY
from database import MongoDBData
import openai
from dotenv import load_dotenv
from Prompts.promptss import linkedin_post_creation_prompt,instagram_post_creation_prompt,email_template_prompt,channel_investment_guidance_prompt,detailed_stategy_development_prompt,digital_marketing_focus_prompt

load_dotenv()  # Load environment variables
openai.api_key = OPENAI_API_KEY
# db = MongoDBData('prompt_db', 'input_prompt')


# Function to generate marketing strategies
def generate_strategy(product_name, product_description, product_category, product_stage, target_audience, region,
                      product_pricing, unique_selling_point, marketing_goals, budget_range, prompts):
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
        else:
            test_prompt = digital_marketing_focus_prompt


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

# Checkbox to select prompts
st.write("Select the actions you want to include:")
selected_prompts = st.multiselect(
    "Choose the marketing strategies to generate:",
    options=["linkedin_post_creation_prompt", "instagram_post_creation_prompt", "email_template_prompt",
             "channel_investment_guidance_prompt", "detailed_stategy_development_prompt",
             "digital_marketing_focus_prompt"],
    default=["linkedin_post_creation_prompt", "instagram_post_creation_prompt", "email_template_prompt"]
)

# Generate button
if st.button("Generate Marketing Strategy"):
    # If no specific prompts are selected, run all
    if not selected_prompts:
        selected_prompts = [
            linkedin_post_creation_prompt,
            instagram_post_creation_prompt,
            email_template_prompt,
            channel_investment_guidance_prompt,
            detailed_stategy_development_prompt,
            digital_marketing_focus_prompt
        ]

    # Generate strategies based on the selected prompts
    print(selected_prompts)
    results = generate_strategy(product_name, product_description, product_category, product_stage,
                                target_audience, region, product_pricing, unique_selling_point,
                                marketing_goals, budget_range, selected_prompts)

    # Parse the results
    st.write(results)
    # # result = re.sub(r'[\x00-\x1F\x7F]', '', results)
    # parser = ResponseParser(results)
    # parsed_instagram = parser.parse_instagram_post()
    # parsed_linkedin = parser.parse_linkedin_post()
    # parsed_email = parser.parse_email_template()
    #
    # # Display the generated marketing strategies
    # st.write("## Generated Marketing Strategy:")
    #
    # if parsed_instagram:
    #     st.subheader("Instagram Post:")
    #     st.write(f"**Action**: {parsed_instagram['action']}")
    #     st.write(parsed_instagram['content'])

    # for prompt, result in results.items():
    #     if "INSTAGRAM_POST" in prompt:
    #         parsed_results['Instagram'] = parser.parse_instagram_post(result)
    #     elif "LINKED_IN_POST" in prompt:
    #         parsed_results['LinkedIn'] = parser.parse_linkedin_post(result)
    #     elif "EMAIL_TEMPLATE" in prompt:
    #         parsed_results['Email'] = parser.parse_email_template(result)
    #
    # # Display the generated marketing strategies
    # st.write("## Generated Marketing Strategy:")
    # for platform, parsed in parsed_results.items():
    #     if parsed:
    #         st.subheader(f"{platform} Post:")
    #         st.write(f"**Action**: {parsed['action']}")
    #         st.write(parsed['content'])
