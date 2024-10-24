import requests
from bs4 import BeautifulSoup as bf

# Function to fetch repository details
def fetch_github_repo_content(url):
    response = requests.get(url)
    soup = bf(response.content, 'html.parser')

    repo_title = soup.find('strong', {'itemprop': 'name'}).text.strip()
    description_tag = soup.find('p', {'itemprop': 'description'})
    repo_description = description_tag.text.strip() if description_tag else 'No description'

    readme_section = soup.find('article', {'itemprop': 'text'})
    readme_content = readme_section.text.strip()[:500] if readme_section else 'No README file'

    file_elements = soup.find_all('a', {'class': 'js-navigation-open Link--primary'})
    files = [file_elem.text.strip() for file_elem in file_elements if file_elem.text.strip()]

    return {
        'repo_name': repo_title,
        'description': repo_description,
        'readme': readme_content,
        'files': files[:10]  # Limit to first 10 files
    }

# New function to search repositories by topic
def search_github_repositories(topic):
    search_url = f"https://github.com/search?q={topic}&type=repositories"
    response = requests.get(search_url)
    soup = bf(response.content, 'html.parser')

    repo_links = soup.find_all('a', {'class': 'v-align-middle'})
    repos = [{'repo_name': repo.text, 'url': f"https://github.com{repo['href']}"} for repo in repo_links[:5]]  # Get top 5 repos

    return repos
