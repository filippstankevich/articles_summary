import yaml
from web_crawler import WebCrawler
from articles_repository import ArticlesRepository
from summary_extractor import SummaryExtractor

if __name__ == '__main__':
    with open('../config.yaml', "r") as yaml_config:
        config = yaml.safe_load(yaml_config)

    extractor = SummaryExtractor(config['openai'])
    repository = ArticlesRepository(config['chromadb'])

    def content_consumer(data):
        print(f'Title: {data['title']}')
        print(f'Content: {data['content']}')
        summary = extractor.extract_summary(data['content'])
        print(f'Summary: {summary}')
        repository.save(data['title'], data['content'], summary)

    crawler = WebCrawler()
    news = crawler.read_articles(config['sources'], content_consumer, depth=1, max_results_per_url=3)

    response = repository.search('Japanese Government')
    print(f'Response: {response}')



