import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag, urlunparse

#GLOBALS
visited = set()
unique_pages = 0

longest_page_url = ''
longest_page_length = 0
common_words = {}

subdomains = {}

def scraper(url, resp):
    try:
        links = extract_next_links(url, resp)
        return [link for link in links if is_valid(link)]
    except Exception as e:
        print(e)
        return []

def extract_next_links(url, resp):
    '''
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    return list()
    '''
    # Handles bad status codes and returns TRUE if not 200
    # Does nothing if 200
    if status_code_bad(resp, url):
        return []
    
    # Tokenize url by / and if anything repeats more than twice, return []
    # We don't need to add to visited
    # http://www.cert.ics.uci.edu/seminar/Nanda/seminar/Nanda/EMWS09/EMWS09/seminar/Nanda/seminar/Nanda/seminar/Nanda/EMWS09/seminar/Nanda/seminar/Nanda/seminar/Nanda/EMWS09/seminar/Nanda/seminar/Nanda/EMWS09/EMWS09/seminar/Nanda/seminar/Nanda/seminar/Nanda/seminar/Nanda/EMWS09/seminar/Nanda/EMWS09/seminar/Nanda/EMWS09/seminar/Nanda/seminar/Nanda/seminar/Nanda/seminar/Nanda/EMWS09/seminar/Nanda/seminar/Nanda/seminar/Nanda/seminar/Nanda/seminar/Nanda/seminar/Nanda/EMWS09/seminar/Nanda/EMWS09/seminar/Nanda/seminar/Nanda/seminar/Nanda/EMWS09/EMWS09/seminar/Nanda/seminar/Nanda/seminar/Nanda/seminar/Nanda/seminar/Nanda/seminar/Nanda/EMWS09/seminar/Nanda/EMWS09/seminar/Nanda/seminar/Nanda/EMWS09/
    if is_long_url(url):
        return []

    # TODO: Use some sort of hashing of html to get similarity score of pages, if score is too high, return []
    if too_similar(resp):
        return []

    # Get valid / defragmented links
    links = get_links(resp, url)

    # Add url without query params to visited
    # Goodlinks check against visited but return full url with query params
    global unique_pages
    goodLinks = filter_query_params(links)

    # We've gotten this far so we can increment our unique pages (might not need this if we have a set of visited urls)
    unique_pages += 1

    # Keeps track of longest page and common words
    handle_word_stuff(resp)
        
    # Keeps track of subdomains in ics.uci.edu. 
    subdomains_tracker(resp)

    return goodLinks

def status_code_bad(resp, url):
    global visited
    # Do stuff if not 200 status code
    if resp.status != 200: 
        # TODO: Index page from redirected crawler
        if resp.status >= 300 and resp.status < 400:
            # HANDLE REDIRECTS
            return True
        
        # 404 error handling
        # TODO: Maybe there is more we can do here?
        print('ERROR:', resp.status)
        visited.add(url_without_query(url)) # This also defragments the url
        return True
    return False


def is_long_url(url):
    url_tokens = url.split('/')
    token_freq = {}
    for token in url_tokens:
        token_freq[token] = token_freq.get(token, 0) + 1
        if token_freq[token] > 2:
            return True
    return False


def too_similar(resp):
    # TODO: Check page similarity via HTML hashing or something
    pass
    



def url_without_query(url): # REMOVE QUERY PARAMETERS
    parsed_url = urlparse(url)
    url_without_query = urlunparse(parsed_url._replace(query="", fragment="")) 
    return url_without_query


def get_links(resp, url):
    links = []
    soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
    for anchor in soup.find_all('a', href=True):
        href = anchor['href'] # get url
        href, _ = urldefrag(href) # deframentation
        href = urljoin(resp.url, href) # getting absolute path
        if is_valid(href) and href != url and href != resp.url: # If valid or not in page
            links.append(href)


def filter_query_params(links):
    global visited
    
    goodLinks = []
    for link in links:
        tempLink = url_without_query(link)
        if tempLink not in visited:
            visited.add(tempLink)
            goodLinks.append(link)

    return goodLinks


def handle_word_stuff(resp):
    global longest_page_url
    global longest_page_length 
    global common_words

    # TODO: utf-8 encoding?
    stopWords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren", "t", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can", "cannot", "could", "couldn", "did", "didn", "do", "does", "doesn", "doing", "don", "down", "during", "each", "few", "for", "from", "further", "had", "hadn", "has", "hasn", "have", "haven", "having", "he", "d", "ll", "s", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "m", "ve", "if", "in", "into", "is", "isn", "it", "its", "itself", "let", "me", "more", "most", "mustn", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan", "she", "should", "shouldn", "so", "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "re", "ve", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn", "we", "were", "weren", "what", "when", "where", "which", "while", "who", "whom", "why", "with", "won", "would", "wouldn", "you", "your", "yours", "yourself", "yourselves"]
    if resp.raw_response.content: #if content exists:
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser') #parsed HTML content
        for script in soup(["script", "style"]): #removes script and style tags from html doc
            script.extract()
        text = soup.get_text()
        # TODO: isalpha?
        words = [word.lower() for word in text.split() if word.isalpha()]

        for word in words:
            if word not in stopWords: #if word is not a stop word and is an english word
                common_words[word] = common_words.get(word, 0) + 1 #increment count if word is already in dict or set to 1 if new

        # Get page length (in length of words) and compare to longest page, if longer, update longest page count and url (BEATUFIUL SOUP)
        if len(words) > longest_page_length:
            longest_page_length = len(words)
            longest_page_url = resp.url


def subdomains_tracker(resp):
    global subdomains

    domain = "ics.uci.edu"
    parsed_url = urlparse(resp.url)
    if parsed_url.hostname.endswith(domain):
        subdomain = parsed_url.hostname[:-len(domain)-1]
        subdomains[subdomain] = subdomains.get(subdomain, 0) + 1


def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if not re.match(r"(.*\.ics\.uci\.edu|.*\.cs\.uci\.edu|.*\.informatics\.uci\.edu|.*\.stat\.uci\.edu)$", parsed.hostname.lower()):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise
