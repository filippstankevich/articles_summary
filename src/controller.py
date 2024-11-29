from flask import request
from articles_service import ArticlesService

from main import web_service

service = ArticlesService()


@web_service.route("/load")
def load_articles():
    depth = request.args.get('depth', default=1)
    max_results_per_url = request.args.get('max_results_per_url', default=3)
    service.load_articles(depth, max_results_per_url)


@web_service.route("/search")
def search():
    query = request.args.get('query')
    return service.search(query)
