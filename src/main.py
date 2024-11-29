import yaml
from flask import Flask

from articles_repository import ArticlesRepository
from articles_service import ArticlesService
from articles_controller import ArticlesController
from summary_extractor import SummaryExtractor
from web_crawler import WebCrawler

if __name__ == '__main__':
    with open('../config.yaml', "r") as yaml_config:
        config = yaml.safe_load(yaml_config)

    openai_config = config['openai']
    summary_extractor = SummaryExtractor(openai_config['api-key'], openai_config['model'])
    articles_repository = ArticlesRepository(config['chromadb']['path'])
    web_crawler = WebCrawler()

    web_app = Flask(__name__)
    articles_service = ArticlesService(summary_extractor, articles_repository, web_crawler, config['sources'])
    articles_controller = ArticlesController(articles_service, web_app)

    web_app.run()
