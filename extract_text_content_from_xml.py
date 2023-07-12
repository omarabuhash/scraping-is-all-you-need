import os
import time
import lxml
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_urls(sitemap_url):
    response = requests.get(sitemap_url)
    xml_content = response.content
    soup = BeautifulSoup(xml_content, 'lxml')
    loc_elements = soup.find_all('loc')
    urls = [loc.text for loc in loc_elements]
    return urls

def retry_get(driver, url):
    retry_count = 5
    retry_delay = 2
    attempts = 0
    while attempts < retry_count:
        try:
            driver.get(url)
            return
        except WebDriverException:
            attempts += 1
            time.sleep(retry_delay)
    raise Exception(f"Failed to get URL: {url}")

def write_core_content_to_directory(url, driver, output_dir):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    try:
        retry_get(driver, url)
        time.sleep(0.5)
        element = driver.find_element(By.ID, "provider-docs-content")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        filepath = os.path.join(output_dir, url.split("/")[-1] + ".txt")
        with open(filepath, "w") as file:
            file.write(f"SOURCE FOR THE FILE: {url}\n\n")
            file.write(element.text)
    except Exception as e:
        print(url)
        print(e)

def run(sitemap_urls, output_dir):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    urls = []
    for sitemap_url in sitemap_urls:
        urls.extend(get_urls(sitemap_url))
    for url in urls:
        write_core_content_to_directory(url, driver, output_dir)
        time.sleep(0.5)
    driver.quit()

if __name__ == "__main__":
    sitemap_urls = ["https://registry.terraform.io/sitemaps/providers-2.xml"]
    output_dir_name = "docs"
    run(sitemap_urls, output_dir_name)