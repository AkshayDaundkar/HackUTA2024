# api.py
import openai
from config import OPENAI_API_KEY

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

def generate_strategy(product_name, product_description, product_category, product_stage, target_audience, region, product_pricing):
    # Create the system message and user message structure for ChatGPT API
    messages = [
        {"role": "system", "content": "You are a marketing expert that helps businesses with market strategies and taglines."},
        {"role": "user", "content": f"""
            Create a marketing strategy for a product with the following details:
            Product Name: {product_name}
            Description: {product_description}
            Category: {product_category}
            Stage: {product_stage}
            Audience: {target_audience}
            Region: {region}
            Pricing: {product_pricing}

            Provide:
            1. A catchy tagline for the product.
            2. A brief market strategy (including positioning and key messaging).
        """}
    ]

    # Make the request to the ChatGPT API using the chat/completions endpoint
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo" if needed
        messages=messages,
        max_tokens=500
    )

    # Extract the reply from the response
    return response['choices'][0]['message']['content']

# Test the API call with sample data
if __name__ == "__main__":
    product_name = "Satan's Breath"
    product_description = "We focus on small-batch brewing techniques to create unique and high-quality India Pale Ales (IPAs). Our business model revolves around offering a diverse range of IPA flavors, catering to niche markets of beer enthusiasts who appreciate bold and distinct tastes."
    product_category = "Beer"
    product_stage = "Launch"
    target_audience = "Young, hipster, late-twenties to late-thirties adult, with an adventurous personality that craves new tastes and experiences."
    region = "Netherlands"
    product_pricing = "Mid-upper range"

    # Call the function to generate strategy
    result = generate_strategy(
        product_name,
        product_description,
        product_category,
        product_stage,
        target_audience,
        region,
        product_pricing
    )

    print("Generated Market Strategy:")
    print(result)
