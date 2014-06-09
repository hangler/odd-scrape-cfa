from bs4 import BeautifulSoup
import requests

BASE_RAW_GITHUB_URL = "https://raw.githubusercontent.com"
CFA_APP_HTML_URL = "https://github.com/codeforamerica/codeforamerica.org/tree/master/_includes/apps"
TAB_FILENAME = "output.tab"

def write(text, tab=True, mode="a"):
    f = open(TAB_FILENAME, mode)
    f.write(text.encode('utf-8'))
    if tab:
        f.write("\t")
    f.close()

def write_headers_to_tab():
    headers = ""
    headers += "cfa_github_page\t"
    headers += "title\t"
    headers += "url\t"
    headers += "summary\t"
    headers += "lang\t"
    headers += "country\t"
    headers += "created_for\t"
    headers += "source_code\t"
    headers += "technology\t"
    for x in range(1, 10):
        headers += "developer_%d\t" % x
    headers += "\n"
    write(headers, tab=False, mode="w")

def parse_title(soup):
    return soup.find('h2').text

def parse_url(soup):
    return soup.find('p', {'class': 'text-whisper'}).find('a').text

def parse_summary(soup):
    for sibling in soup.find('h3').next_siblings:
        try:
            return sibling.text
        except AttributeError:
            pass

def parse_developers(soup):
    people = []
    try:
        for bullet in soup.findAll('ul')[0].findAll('li'):
            developer = bullet.find('a').text
            people.append(developer)
        return people
    except AttributeError:
        return people

def parse_created_for(soup):
    try:
        return soup.findAll('ul')[1].find('li').find('a').text
    except IndexError:
        return ""

def parse_source_code(soup):
    try:
        for row in soup.find('table', {'class': 'table-minor'}).findAll('tr'):
            if "Codebase" in row.find('th').text:
                return row.find('a').get('href')
        return ""
    except IndexError:
        return ""

def parse_technology(soup):
    try:
        for row in soup.find('table', {'class': 'table-minor'}).findAll('tr'):
            if "Environment" in row.find('th').text:
                return row.find('td').text
        return ""
    except IndexError:
        return ""

def parse_app_page(page_url):
    print "Accessing page %s" % page_url
    page = requests.get(page_url).text
    soup = BeautifulSoup(page)
    write(page_url)
    write(parse_title(soup))        # App Title
    write(parse_url(soup))          # App URL
    write(parse_summary(soup))      # Summary
    write("EN")                     # Language
    write("USA")                    # Country
    write(parse_created_for(soup))
    write(parse_source_code(soup))
    write(parse_technology(soup))
    write("\t".join(parse_developers(soup)))    # Developers
    write("\n", tab=False)

def main():

    write_headers_to_tab()

    page = requests.get(CFA_APP_HTML_URL).text
    soup = BeautifulSoup(page)

    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        link_to_app_page = row.findAll('td')[1].findAll('a')[0].get('href')
        link_to_app_page = link_to_app_page.replace("/blob", "")
        page_url = BASE_RAW_GITHUB_URL + link_to_app_page
        parse_app_page(page_url)

    write("\n")

main()



# https://raw.githubusercontent.com/codeforamerica/codeforamerica.org/master/_includes/apps/adopt-a-hydrant.html
# https://raw.githubusercontent.com/codeforamerica/codeforamerica.org/master/_includes/apps/adopt-a-hydrant.html#