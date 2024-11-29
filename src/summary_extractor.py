from openai import OpenAI


class SummaryExtractor:

    def __init__(self, api_key, model):
        self._api_key = api_key
        self._model = model

    def extract_summary(self, content):
        # todo we should chunk large content before sending to open ai

        messages = [
            {"role": "system", "content": "Rewrite this text in summarized form."},
            {"role": "user", "content": content}
        ]

        client = OpenAI(api_key=self._api_key)

        response = client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=0
        )

        return response.choices[0].message.content