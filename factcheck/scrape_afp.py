from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .scrape_post import scrape_post
from .store_text import save_to_txt

def scrape_afp(posts_num, afp_url, filename):
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)
    browser.maximize_window()
    wait = WebDriverWait(browser, 10)
    posts = []

    try:
        browser.get(afp_url)
        
        iteration = 0
        last_post_index = 0

        while len(posts) < posts_num:
            posts_html = wait.until(EC.visibility_of_all_elements_located(
                (By.XPATH, "//article[contains(@class, 'node node--type-article node--promoted node--view-mode-teaser')]")
            ))

            for i in range(last_post_index, len(posts_html)):
                element = posts_html[i]
                post_url = element.find_element(By.TAG_NAME, "a").get_attribute("href")
                posts.append(post_url)
                post_text = scrape_post(post_url)
                print(post_text)
                save_to_txt(post_url, post_text, filename)

                if len(posts) >= posts_num:
                    break

            # Click on See more to load the rest if needed!
            last_post_index = len(posts)
            if last_post_index < posts_num:
                try:
                    show_more_btn = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//a[contains(@title, 'Load more items')]")
                    ))
                    browser.execute_script("arguments[0].click()", show_more_btn)
                    wait.until(EC.invisibility_of_element_located(
                        (By.XPATH, "//a[contains(@title, 'Load more items') and @disabled]")
                    ))
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                except TimeoutException:
                    pass

            iteration += 1

    finally:
        browser.quit()
        
    return posts
