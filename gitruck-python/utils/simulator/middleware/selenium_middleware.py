import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def forced_wait(
        base_time=1
):
    time.sleep(round(base_time + random.random(), 2))


def explicit_wait(
        driver,
        xpath,
        timeout=60,
        pf=0.5,
        iv=True,
):
    if iv:

        # 每隔0.5s检查一次(默认就是0.5s), 最多等待60秒
        element = WebDriverWait(driver, timeout, pf).until(
            EC.visibility_of_element_located(
                (By.XPATH, xpath)
            )
        )
    else:

        # 两种写法，都可以采用
        # element = WebDriverWait(driver, timeout, pf).until_not(
        #     EC.visibility_of_element_located(
        #         (By.XPATH, xpath)
        #     )
        # )

        element = WebDriverWait(driver, timeout, pf).until(
            EC.invisibility_of_element_located(
                (By.XPATH, xpath)
            )
        )

    return element


def is_element_exist_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
        return True
    except Exception as e:
        print(e)
        return False


def continuous_click_until_elem_disappear(
        driver,
        xpath,
        pf=5,
):
    while True:
        try:
            driver.find_element(By.XPATH, xpath).click()
        except Exception as e:
            print(e)
        time.sleep(pf)
        if not is_element_exist_by_xpath(driver, xpath):
            break


class SeleniumMiddleware(object):

    def __init__(self):
        print(self)


if __name__ == "__main__":
    sm = SeleniumMiddleware()
    # sm.run()
