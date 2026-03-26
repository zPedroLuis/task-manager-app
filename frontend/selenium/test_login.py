import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.e2e
def test_login_page_loads():
    selenium_url = os.getenv("SELENIUM_URL")
    if not selenium_url:
        pytest.skip("Defina SELENIUM_URL para executar os testes Selenium.")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(command_executor=selenium_url, options=options)
    try:
        driver.get("http://localhost:5173/login")
        title = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "h1"))
        )
        assert title.text == "Entrar"
    finally:
        driver.quit()
