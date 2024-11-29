from flask import Flask
from articles_service import ArticlesService
from controller import web_service

if __name__ == '__main__':
    # service = ArticlesService()
    # service.load_articles()
    #
    # response = service.search('Japanese Government')
    # print(f'Response: {response}')

    web_service.run()
