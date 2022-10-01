import json
import os
import requests


class ProxyMiddleware(object):

    def __init__(self):

        with open("utils/simulator/config.json", 'r') as f0:
            self.info = json.load(f0)

    def oversea_proxy_middleware(self):
        return self.info["gfw_proxy_url"]

    def random_proxy_middleware(self):
        proxy_url = self.info["proxy_pool_url"]
        response = requests.get(proxy_url)
        return 'http://' + response.text


if __name__ == "__main__":
    pm = ProxyMiddleware()
    pm.oversea_proxy_middleware()
