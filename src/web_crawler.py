from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class WebCrawler:
    def read_articles(self, urls: list[str], content_consumer, depth=1, max_results_per_url=100) -> int:
        total = 0
        for url in urls:
            processed = self._process_url(url, content_consumer, depth, max_results_per_url)
            total = total + processed
        return total

    def _process_url(self, url: str, content_consumer, max_depth, max_results):

        # we traverse web page using BFS
        queue = [(url, 0)]  # root node has 0 depth
        processed = 0
        while queue:
            (link, depth) = queue.pop(0)
            if self._is_a_news_link(link) and processed < max_results:
                #  for now, we process at the time of traversing,
                #  but it can be done separately, and in multiple threads
                article = self._proccess_article_link(link)
                if article:
                    content_consumer(article)
                    processed += 1
                    print(f'Articles processed: {processed}')

            if depth < max_depth and processed < max_results:
                html = requests.get(url).text
                soup = BeautifulSoup(html, 'lxml')
                links = soup.find_all('a')

                new_depth = depth + 1
                for new_link in links:
                    full_link = urljoin(url, new_link['href'])
                    queue.append((full_link, new_depth))

        return processed

    # for now, it will probably work with bbc news, but you may somehow customize it using inheritance or config file
    def _is_a_news_link(self, link):
        return 'article' in link

    def _proccess_article_link(self, link):
        subpage_html = requests.get(link).text
        page = BeautifulSoup(subpage_html, 'lxml')

        title = page.find('title').text
        p_elements = page.find_all('p')
        paragraphs = []
        for paragraph in p_elements:
            paragraphs.append(paragraph.text)

        return {
            'title': title,
            'content': '\n'.join(paragraphs),
            'link': link
        } if paragraphs else None
