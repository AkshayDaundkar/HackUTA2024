# api.py
from LLM.llm import generate_strategy
from Parsers.response_parser import ResponseParser
import re
if __name__ == "__main__":
    product_name = "TexSneaks"
    product_description = "TexSneaks offers trendy, high-quality, and eye-catching sneakers that are perfect for fashion-forward teenagers. With bold designs and vibrant colors, our shoes stand out from the crowd and help young people express their individuality. Our collection includes limited-edition drops and collaborations with local artists."
    product_category = "Shoes"
    product_stage = "Launch"
    target_audience = "Teenagers aged 13-19, fashion-conscious, interested in streetwear, and looking for bold, statement shoes that reflect their unique personalities."
    region = "Texas"
    product_pricing = "Mid-range to high-end"
    unique_selling_point = "No competition in market right now"
    marketing_goals = "To sell 1000 pieces per day"
    budget_range = "20 USD"

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

    print("Generated Market Strategy:")
    print(result)

    # result.replace("\n", "").replace("\t", "").replace("\r", "")
    result=re.sub(r'[\x00-\x1F\x7F]', '', result)
    parser = ResponseParser(result)
    # parsed_linked_post= parser.parse_linkedin_post()
    #parsed_instagram_post = parser.parse_instagram_post()
    parsed_email = parser.parse_linkedin_post()


    if parsed_email:
        print("Parsed LinkedIn Post:")
        print(f"Action: {parsed_email['action']}")
        print(f"Content: {parsed_email['content']}")
