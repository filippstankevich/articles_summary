import yaml
from web_crawler import WebCrawler
from articles_repository import ArticlesRepository
from summary_extractor import SummaryExtractor


class ArticlesService:
    def __init__(self):
        with open('../config.yaml', "r") as yaml_config:
            self._config = yaml.safe_load(yaml_config)

        self._extractor = SummaryExtractor(self._config['openai'])
        self._repository = ArticlesRepository(self._config['chromadb'])
        self._crawler = WebCrawler()

    def load_articles(self, depth=1, max_per_url=3):
        return self._crawler.read_articles(self._config['sources'], self._content_consumer, depth, max_per_url)

    def search(self, query):
        return self._repository.search(query)

    def _content_consumer(self, data):
        print(f'Title: {data['title']}')
        print(f'Content: {data['content']}')
        summary = self._extractor.extract_summary(data['content'])
        print(f'Summary: {summary}')
        self._repository.save(data['title'], data['content'], summary)