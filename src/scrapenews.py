from selenium import webdriver
from json import dumps
from redis import Redis
from cached_property import cached_property
import time

CATEGORIES = ["energy", "financial", "healthcare", "business_services", "telecom_utilities", "cannabis",
              "hardware_electronics", "software_services", "industrials", "manufacturing_materials",
              "consumer_products_media", "diversified_business", "retailing_hospitality"]
ROOT_URL = "https://ca.finance.yahoo.com/industries/"
ROOT_URL_CANNABIS = "https://ca.finance.yahoo.com/topic/cannabis/"


class ScrapeNews:
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)
    driver.implicitly_wait(3)

    @cached_property
    def _get_redis(self):
        return Redis(host='redis', port=6379)

    def scrape(self, category: str) -> list:
        if category not in CATEGORIES:
            raise CategoryDoesNotExist
        if category == "cannabis":
            root_url = ROOT_URL_CANNABIS
        else:
            root_url = ROOT_URL + category
        self.driver.get(root_url)
        for i in range(0, 3):
            self.driver.execute_script('window.scrollBy(0, 600)')
            time.sleep(1)
        article_blocks = self.driver.find_elements_by_xpath("//div[@class='Cf']")
        articles = []
        for block in article_blocks:
            children = block.find_elements_by_xpath("*")
            summary = children[1] if len(children) == 3 else children[0]
            title = summary.find_element_by_xpath("h3/a")
            title_text = title.text
            url = title.get_attribute('href')
            body = summary.find_element_by_xpath("p").text
            body = body[:250] + "..." if len(body) > 200 else body
            articles.append({"title": title_text, "body": body, "url": url})
        redis = self._get_redis
        redis.set(category, dumps(articles), ex=900)
        return articles


class CategoryDoesNotExist(Exception):
    pass
