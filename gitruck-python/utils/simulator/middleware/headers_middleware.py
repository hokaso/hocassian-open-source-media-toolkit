from fake_useragent import UserAgent


def random_headers():
    ua = UserAgent()
    return ua.random


class HeadersMiddleware(object):
    pass


if __name__ == "__main__":
    random_headers()
