import uuid

import chromadb
from chromadb.utils import embedding_functions


class ArticlesRepository:

    def __init__(self, config):
        self._client = chromadb.PersistentClient(path=config['path'])

        self._collection = self._client.get_or_create_collection(
            'articles',
            # todo is there a better embedding model? openai?
            embedding_function=embedding_functions.DefaultEmbeddingFunction())

    def save(self, title, content, summary):
        # todo not ideal, title and summary will have same importance when searching
        # todo should we store content in different connection?
        self._collection.add(documents=[title + '\n' + summary], ids=[str(uuid.uuid4())], metadatas={'title': title, 'content': content})

    def search(self, phrase):
        return self._collection.query(query_texts=[phrase], n_results=1)['documents'][0][0]
