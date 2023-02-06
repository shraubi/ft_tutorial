import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from db import create_table, get_engine, get_session, samples

logging.basicConfig(level=logging.INFO)
browser = Service(ChromeDriverManager().install())


def get_driver() -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    return webdriver.Chrome(service=browser, options=chrome_options)


def parse(session):
    driver = get_driver()
    link = "PATH_TO_PAGE"
    driver.get(link)
    for i in link:
        print(driver.current_url)
        msg = driver.find_elements(
            By.XPATH, "//*[text()[contains(.,'NAME')]]/following-sibling::*[2]"
        )
        for uno in msg:
            if len(uno.text) > 140:
                new_row = samples(text=uno.text)
                choose = session.query(samples).filter(samples.text == uno.text).first()
                if choose:
                    continue
                else:
                    session.add(new_row)
                    session.commit()
            else:
                continue
        driver.find_element(
            By.XPATH,
            "//*[contains(@class, 'pagination block_link') and contains(text(), 'Next messages')]",
        ).click()


def main():
    engine = get_engine()
    create_table(engine)
    session = get_session(engine)
    parse(session)
    session.close()


if __name__ == "__main__":
    main()
