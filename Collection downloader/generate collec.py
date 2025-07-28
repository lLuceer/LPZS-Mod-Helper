import requests
from bs4 import BeautifulSoup

def get_workshop_links(collection_id, output_file='workshop_links.txt'):
    url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={collection_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"[!] Failed to fetch page. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    # Look for all divs with class 'collectionItem' — newer layout
    for div in soup.find_all('div', class_='collectionItem'):
        link_tag = div.find('a', href=True)
        if link_tag and 'filedetails/?id=' in link_tag['href']:
            full_link = 'https://steamcommunity.com' + link_tag['href']
            links.append(full_link)

    if not links:
        print("[!] No workshop items found. Steam layout may have changed.")
        return

    with open(output_file, 'w') as f:
        for link in links:
            f.write(link + '\n')

    print(f"[+] Saved {len(links)} workshop links to {output_file}")

# Example usage:
if __name__ == "__main__":
    collection_id = input("Enter Steam collection ID: ").strip()
    get_workshop_links(collection_id)
