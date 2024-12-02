from flask import request, Flask


class ArticlesController:

    def __init__(self, articles_service, app: Flask):
        self._articles_service = articles_service
        app.add_url_rule("/load", view_func=self._load_articles)
        app.add_url_rule("/search", view_func=self._search)

    def _load_articles(self):
        depth = request.args.get('depth', default=1)
        max_results_per_url = int(request.args.get('max', default=20))
        total = self._articles_service.load_articles(depth, max_results_per_url)
        return {'message': f'Successfully loaded {total} articles'}

    def _search(self):
        query = request.args.get('query')
        if not query:
            return {'error': "No 'query' parameter provided"}
        max_results = int(request.args.get('max', default=1))
        results = self._articles_service.search(query, max_results)
        return {'results': [result.__dict__ for result in results]}
