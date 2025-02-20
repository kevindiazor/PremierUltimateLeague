import trafilatura

def analyze_wul_site():
    url = "https://westernultimateleague.shinyapps.io/stats/"
    downloaded = trafilatura.fetch_url(url)
    content = trafilatura.extract(downloaded)
    return content

if __name__ == "__main__":
    content = analyze_wul_site()
    print(content)
