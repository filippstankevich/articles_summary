from openai import OpenAI


class SummaryExtractor:

    def __init__(self, config):
        self._config = config

    def extract_summary(self, content):
        # todo we should chunk large content before sending to open ai

        messages = [
            {"role": "system", "content": "Rewrite this text in summarized form."},
            {"role": "user", "content": content}
        ]

        client = OpenAI(api_key=self._config['api-key'])

        response = client.chat.completions.create(
            model=self._config['model'],
            messages=messages,
            temperature=0
        )

        return response.choices[0].message.content