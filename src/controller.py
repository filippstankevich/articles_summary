from flask import request, Flask
from articles_service import ArticlesService

web_service = Flask(__name__)
service = ArticlesService()


@web_service.route("/load")
def load_articles():
    depth = request.args.get('depth', default=1)
    max_results_per_url: int = request.args.get('max', default=3)
    total = service.load_articles(depth, max_results_per_url)
    return { 'message' : f'Successfully loaded {total} articles' }


@web_service.route("/search")
def search():
    query = request.args.get('query')
    if not query:
        return { 'error' : "No 'query' parameter provided" }
    max_results: int = request.args.get('max', default=3)
    results = service.search(query, max_results)
    return { 'results': [ result.__dict__ for result in results ] }