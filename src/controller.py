from flask import request, Flask
from articles_service import ArticlesService

web_service = Flask(__name__)
service = ArticlesService()


@web_service.route("/load")
def load_articles():
    depth = request.args.get('depth', default=1)
    max_results_per_url = request.args.get('max_per_url', default=3)
    total = service.load_articles(depth, max_results_per_url)
    return f'Successfully loaded {total} articles'


@web_service.route("/search")
def search():
    query = request.args.get('query')
    return service.search(query) if query else "No 'query' parameter provided"
