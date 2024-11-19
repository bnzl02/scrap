from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def scrape_post(post_url):
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)
    wait = WebDriverWait(browser, 10)
    paragraphs = []

    try:
        browser.get(post_url)

        wrapper_body = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "wrapper-body")
        ))

        content_div = wrapper_body.find_element(By.XPATH, ".//div[contains(@class, 'clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item')]")

        paragraphs_elements = content_div.find_elements(By.TAG_NAME, "p")

        for p in paragraphs_elements:
            paragraphs.append(p.text.strip())

    except TimeoutException:
        print(f"Timeout occurred while loading {post_url}")
        paragraphs = []

    finally:
        browser.quit()

    return paragraphs
