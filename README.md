# Scraping is all you need
Scrape a website's entire text content from a list of sitemap.xml urls.

1) Get the sitemap.xml url by appending `/sitemap.xml` to the url you're interested in or appending `/robots.txt` to the url to view all sitemaps for the given url.
2) Update the `sitemap_urls` array and the `output_dir_name` variable in the script.
3) Run the script: `python3 extract_text_content_from_xml.py`
