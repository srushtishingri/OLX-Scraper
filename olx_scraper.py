import requests
from bs4 import BeautifulSoup
import json
import time
import random

def search_olx(query):
    """
    Search OLX for the given query and save results to a file
    """
    print(f"Searching OLX for: {query}")
    url = f"https://www.olx.in/items/q-{query.replace(' ', '-')}"
    print(f"Fetching from URL: {url}")
    
    # Add headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all product listings
        # Note: These selectors may need adjustment based on OLX's current HTML structure
        listings = soup.find_all('li', {'data-aut-id': 'itemBox'})
        
        if not listings:
            print("No listings found. The selector might need to be updated.")
            # Try alternative selectors
            listings = soup.select('.EIR5N')
        
        results = []
        for listing in listings:
            try:
                title_elem = listing.find('span', {'data-aut-id': 'itemTitle'}) or listing.select_one('.IKo3_')
                price_elem = listing.find('span', {'data-aut-id': 'itemPrice'}) or listing.select_one('._2Ks63')
                location_elem = listing.find('span', {'data-aut-id': 'item-location'}) or listing.select_one('._1KOFM')
                link_elem = listing.find('a')
                
                title = title_elem.text.strip() if title_elem else "No title"
                price = price_elem.text.strip() if price_elem else "No price"
                location = location_elem.text.strip() if location_elem else "No location"
                link = link_elem['href'] if link_elem and 'href' in link_elem.attrs else ""
                
                # Make sure the link is absolute
                if link and link.startswith('/'):
                    link = f"https://www.olx.in{link}"
                
                results.append({
                    'title': title,
                    'price': price,
                    'location': location,
                    'link': link
                })
            except Exception as e:
                print(f"Error parsing listing: {e}")
        
        # Save results to file
        output_file = 'olx_car_cover_results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"Found {len(results)} results")
        print(f"Results saved to {output_file}")
        
        # Display first few results as preview
        print("\nSample results:")
        for i, item in enumerate(results[:3]):
            print(f"\n--- Item {i + 1} ---")
            print(f"Title: {item['title']}")
            print(f"Price: {item['price']}")
            print(f"Location: {item['location']}")
            print(f"Link: {item['link']}")
        
        return results
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from OLX: {e}")
        return []

if __name__ == "__main__":
    search_olx("car-cover")