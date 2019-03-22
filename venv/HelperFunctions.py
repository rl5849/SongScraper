
#Helper method to find the ajax call that renders the songs into the container
# 1. Searches for all the script tags, then extracts all the urls in them
# 2. Looks on each page for the container name
# Param : container - Name of the container that is being loaded into
def FindContainer(self, container):
    js_links = []
    container_containing_pages = []
    content = requests.get(secrets.Station_URL).content

    soup = BeautifulSoup(content, 'html.parser')
    js_tags = soup.findAll("script")
    print("Found " + str(len(js_tags)) + " tags")

    for tag in js_tags:
        link = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+.*?(?=\")', str(tag))
        if(len(link) > 0):
            js_links.append(link)

    for link in js_links:
        content_child = requests.get(link).content
        occurances = re.findall(container, content_child)
        if (len(occurances) > 0):
            container_containing_pages.append(link)

    return container_containing_pages