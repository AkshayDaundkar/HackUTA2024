import json
import xml.etree.ElementTree as ET


class ResponseParser:
    def __init__(self, response_str):
        self.response_str = response_str

    def _parse_response(self):
        try:
            root = ET.fromstring(self.response_str)
            response_json_str = root.find('response').text.strip()
            return json.loads(response_json_str)
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None

    def parse_instagram_post(self):
        response_json = self._parse_response()
        if response_json:
            return {
                "action": response_json.get('action'),
                "content": response_json.get('response')
            }
        return None

    def parse_linkedin_post(self):
        response_json = self._parse_response()
        if response_json:
            return {
                "action": response_json.get('action'),
                "content": response_json.get('response')
            }
        return None

    def parse_email_template(self):
        response_json = self._parse_response()
        if response_json:
            return {
                "action": response_json.get('action'),
                "content": response_json.get('response')
            }
        return None


# Example usage (to be removed in production)
