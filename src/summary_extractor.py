import tiktoken
from openai import OpenAI


class SummaryExtractor:

    def __init__(self, api_key, model):
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def extract_summary(self, content, recursive_summary=True):
        chunks = self._get_chunks(content)

        previous_summaries = []
        for chunk in chunks:
            if recursive_summary and previous_summaries:
                total_summary = ' '.join(previous_summaries)
                user_message_content = f'Previous summaries:\n{total_summary}\nText to summarize next:\n{chunk}'
            else:
                user_message_content = chunk

            messages = [
                {'role': 'system', 'content': 'Rewrite this text in summarized form.'},
                {'role': 'user', 'content': user_message_content}
            ]

            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=0
            )

            previous_summaries.append(response.choices[0].message.content)

        return ' '.join(previous_summaries)

    def _get_chunks(self, text, desired_tokens_per_chunk=2048) -> list[str]:
        encoding = tiktoken.encoding_for_model(self._model)
        total_tokens = len(encoding.encode(text))
        total_chunks = round(total_tokens / desired_tokens_per_chunk)
        if total_chunks <= 1:
            return [text]

        ## doing approximate chunks splitting based on calculated number of chunks
        chunk_size_in_chars = round(len(text) / total_chunks)
        chunks = []
        current_chunk = ""
        for sentence in text.split("."):
            current_chunk += sentence + "."
            if len(current_chunk) >= chunk_size_in_chars:
                chunks.append(current_chunk)
                current_chunk = ""

        if current_chunk:
            chunks.append(current_chunk)

        return chunks
