import uuid

import chromadb
from chromadb.utils import embedding_functions

from search_result import SearchResult


class ArticlesRepository:

    def __init__(self, path):
        self._client = chromadb.PersistentClient(path=path)

        self._collection = self._client.get_or_create_collection(
            'articles',
            # todo is there a better embedding model? openai?
            embedding_function=embedding_functions.DefaultEmbeddingFunction())

    def save(self, title, content, summary):
        # todo should we store content in different connection?
        self._collection.add(documents=[self._encode_document(title, summary)], ids=[str(uuid.uuid4())], metadatas={'title': title, 'content': content})

    def search(self, phrase, max_results) -> list[SearchResult]:
        query_result = self._collection.query(query_texts=[phrase], n_results=max_results)
        size = len(query_result['documents'][0])

        search_results = []
        for i in range(size):
            document = query_result['documents'][0][i]
            metadata = query_result['metadatas'][0][i]
            distance = query_result['distances'][0][i]
            search_result = SearchResult(metadata['title'], metadata['content'], self._extract_summary(document), distance)
            search_results.append(search_result)

        return search_results

    def _encode_document(self, title, summary):
        # todo not ideal, title and summary will have same importance when searching
        return title + '\n' + summary

    def _extract_summary(self, document: str):
        if '\n' not in document:
            return document

        return document[document.index('\n') + 1:len(document)]


