import os
import requests
from bs4 import BeautifulSoup
import re
import time
import random

def get_headers():
    """Return a realistic browser headers dictionary with random user agent"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
    ]
    
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.google.com/',
        'DNT': '1'
    }

def bypass_security(url):
    """Attempt to bypass common security measures"""
    session = requests.Session()
    
    # Configure session with headers and cookies
    session.headers.update(get_headers())
    
    # Add common cookies that might be expected
    session.cookies.update({
        'session_id': ''.join(random.choices('abcdef0123456789', k=32)),
        'consent': 'true',
        'accept_cookies': '1'
    })
    
    # Random delay to mimic human behavior
    time.sleep(random.uniform(1, 3))
    
    try:
        response = session.get(url, timeout=30)
        
        # Check for Cloudflare protection
        if 'cloudflare' in response.headers.get('server', '').lower():
            print("\n[!] Cloudflare protection detected. Trying to bypass...")
            # Add additional headers that might help
            session.headers.update({
                'CF-IPCountry': 'US',
                'CF-Connecting_IP': '192.168.1.1'  # Fake IP
            })
            response = session.get(url, timeout=30)
        
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"\n[!] Error accessing the URL: {e}")
        return None

def clean_filename(filename):
    """Remove invalid characters from filename"""
    return re.sub(r'[\\/*?:"<>|]', '', filename)

def save_content(content, filepath):
    """Save content to file with error handling"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except IOError as e:
        print(f"\n[!] Error saving file: {e}")
        return False

def main():
    print("=== Advanced Web Scraper ===")
    print("This program scrapes website content and saves it to a text file.")
    print("Note: Use this tool responsibly and comply with website terms of service.\n")
    
    # Get URL from user
    url = input("Enter the URL to scrape (include http:// or https://): ").strip()
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    print("\n[+] Connecting to the website...")
    response = bypass_security(url)
    
    if response is None:
        print("\n[!] Failed to access the website. Exiting...")
        return
    
    if response.status_code != 200:
        print(f"\n[!] Received HTTP {response.status_code} response. The website may have blocked the request.")
        print("[!] You may want to try again later or use a proxy/VPN.")
    
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Get pretty-printed HTML
    pretty_html = soup.prettify()
    
    # Get user preferences for saving
    print("\n[+] Where would you like to save the scraped content?")
    default_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
    save_dir = input(f"Enter directory path (leave blank for {default_dir}): ").strip()
    save_dir = save_dir if save_dir else default_dir
    
    # Create directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    # Get filename
    default_name = clean_filename(url.split('//')[1].split('/')[0].replace('.', '_')) + '.txt'
    filename = input(f"Enter filename (leave blank for {default_name}): ").strip()
    filename = filename if filename else default_name
    
    # Ensure .txt extension
    if not filename.lower().endswith('.txt'):
        filename += '.txt'
    
    # Save the content
    filepath = os.path.join(save_dir, clean_filename(filename))
    print(f"\n[+] Saving content to: {filepath}")
    
    if save_content(pretty_html, filepath):
        print("[+] Content saved successfully!")
    else:
        print("[!] Failed to save content.")

if __name__ == "__main__":
    main()