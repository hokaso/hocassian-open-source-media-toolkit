from importlib import import_module
from utils.simulator.middleware.headers_middleware import random_headers
from utils.simulator.middleware.proxy_middleware import ProxyMiddleware


class SeleniumInitialize(object):
    default_headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    pm = ProxyMiddleware()

    # 优先级：proxy > use_oversea_proxy > use_random_proxy | headers > use_random_headers
    def __init__(
            self,
            driver_name="chrome",
            use_oversea_proxy=False,
            use_random_proxy=False,
            use_random_headers=False,
            headers=None,
            proxy=None,
            driver_executable_path=None,

            # driver_arguments=None,
            # browser_executable_path=None,
    ):
        """Initialize the selenium webdriver

        Parameters
        ----------
        driver_name: str
            The selenium ``WebDriver`` to use
        driver_executable_path: str
            The path of the executable binary of the driver
        """

        webdriver_base_path = f'selenium.webdriver.{driver_name}'

        driver_klass_module = import_module(f'{webdriver_base_path}.webdriver')
        driver_klass = getattr(driver_klass_module, 'WebDriver')

        driver_options_module = import_module(f'{webdriver_base_path}.options')
        driver_options_klass = getattr(driver_options_module, 'Options')

        driver_options = driver_options_klass()

        # if browser_executable_path:
        #     driver_options.binary_location = browser_executable_path

        # if driver_arguments:
        #     for argument in driver_arguments:
        #         driver_options.add_argument(argument)

        if not headers:
            if use_random_headers:
                headers = random_headers()
            else:
                headers = self.default_headers

        user_agent = 'user-agent=%s' % headers
        driver_options.add_argument(user_agent)

        if not proxy:
            if use_oversea_proxy:
                proxy = self.pm.oversea_proxy_middleware()
            elif use_random_proxy:
                proxy = self.pm.random_proxy_middleware()

        if proxy:
            proxy_arg = '--proxy-server=%s' % proxy
            driver_options.add_argument(proxy_arg)

        driver_kwargs = {
            f'{driver_name}_options': driver_options
        }

        if driver_executable_path:
            driver_kwargs["executable_path"] = driver_executable_path

        self.driver = driver_klass(**driver_kwargs)

        # https://cdn.jsdelivr.net/gh/requireCool/stealth.min.js/stealth.min.js
        with open('utils/simulator/stealth.min.js', 'r') as f:
            js = f.read()

        # 调用函数在页面加载前执行脚本
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': js})

    def handler(self):
        return self.driver
