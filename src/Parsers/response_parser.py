import json
import re

class ResponseParser:
    def __init__(self, response_str):
        self.response_str = response_str

    def _parse_response(self):
        """Helper method to extract JSON content using regex."""
        # Regular expression to extract the JSON part from the response
        json_match = re.search(r'<response>(.*?)</response>', self.response_str, re.DOTALL)
        if json_match:
            json_content = json_match.group(1).strip()
            try:
                return json.loads(json_content)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return None
        else:
            print("No valid JSON content found in the response.")
            return None

    def parse_instagram_post(self):
        """Parse the response for an Instagram post."""
        response_json = self._parse_response()
        if response_json:
            return {
                "action": response_json.get('action'),
                "content": response_json.get('response')
            }
        return None

    def parse_linkedin_post(self):
        """Parse the response for a LinkedIn post."""
        response_json = self._parse_response()
        if response_json:
            return {
                "action": response_json.get('action'),
                "content": response_json.get('response')
            }
        return None

    def parse_email_template(self):
        """Parse the response for an email template."""
        response_json = self._parse_response()
        if response_json:
            return {
                "action": response_json.get('action'),
                "content": response_json.get('response')
            }
        return None


