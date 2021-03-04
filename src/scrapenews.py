from selenium import webdriver
import time


class ScrapeNews:
    CATEGORIES = ["energy", "financial", "healthcare", "business_services", "telecom_utilities", "cannabis",
                  "hardware_electronics", "software_services", "industrials", "manufacturing_materials",
                  "consumer_products_media", "diversified_business", "retailing_hospitality"]
    ROOT_URL = "https://ca.finance.yahoo.com/industries/"
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium-freeworld"
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)
    driver.implicitly_wait(3)

    def __init__(self, category: str):
        if category not in self.CATEGORIES:
            raise CategoryDoesNotExist
        self.category = category

    def scrape(self) -> list:
        self.driver.get(self.ROOT_URL + self.category)
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
        return articles


class CategoryDoesNotExist:
    pass
