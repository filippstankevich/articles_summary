class ArticlesService:
    def __init__(self, summary_extractor, articles_repository, web_crawler, sources):
        self._summary_extractor = summary_extractor
        self._articles_repository = articles_repository
        self._web_crawler = web_crawler
        self._sources = sources

    def load_articles(self, depth=1, max_per_url=3):
        return self._web_crawler.read_articles(self._sources, self._content_consumer, depth, max_per_url)

    def search(self, query, max_results=1):
        return self._articles_repository.search(query, max_results)

    def _content_consumer(self, data):
        print(f'Title: {data['title']}')
        print(f'Content: {data['content']}')
        summary = self._summary_extractor.extract_summary(data['content'])
        print(f'Summary: {summary}')
        self._articles_repository.save(data['title'], data['content'], summary)