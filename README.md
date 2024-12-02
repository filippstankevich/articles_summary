# Articles summariser

## How to use

1. Install required dependencies specified in *requirements.txt*
2. Put your OpenAI API key in *config.yaml*
3. Run *main.py*
4. Perform initial load calling http://127.0.0.1:5000/load
5. Perform search using http://127.0.0.1:5000/search?query=phrase

### Notes

- */load* by default loads first 20 articles, you may tune it by passing param ```max=<desired value>```.
It works per url to be crawled

- */search* by default returns top 1 result, you may tune it by passing ```max=<desired value>```.

- All REST API intentionally use GET methods for your convenience if you don't have Postman or other tools installed

- By default, app runs on *5000* port, you can override it in 'config.yaml'

- The application written using Python 3.13

### Limitations

Since there was no goal of production ready app, this application was tested on 'BBC news' source only.
Each news website might have own specific markup. The web crawler needs a further tuning for other sources.

### Further improvements

- Support of different sources
- Concurrent web crawling