import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag

#Counters
visited = set()
crawled = 0
unique_pages = 0
frequencies = {}
page_lengths = {}
subdomains = {}

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

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
    #Add to Visited
    global visited
    visited.add(url)
    visited.add(resp.url)
    #Problem with Status Code
    if (resp.status != 200):
        return []

    #Main Scraper
    links = []
    try:
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
    except:
        return links
    for anchor in soup.find_all('a', href=True):
        href = anchor['href']
        href, _ = urldefrag(href)
        href = urljoin(resp.url, href)
        links.append(href)
    '''
    #Helps with frequencies
    content = str(resp.raw_response.content)
    tokens = []
    current_token = ""
    for char in content:
        if (('a' <= char <= 'z') or ('A' <= char <= 'Z')):
            current_token += char.lower()
        else:
            if current_token != "":
                tokens.append(current_token)
                current_token = ""
    for token in tokens[:]:
        #Filters out English Stopwords and HTML Markup
        if (token in ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren", "t", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can", "cannot", "could", "couldn", "did", "didn", "do", "does", "doesn", "doing", "don", "down", "during", "each", "few", "for", "from", "further", "had", "hadn", "has", "hasn", "have", "haven", "having", "he", "d", "ll", "s", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "m", "ve", "if", "in", "into", "is", "isn", "it", "its", "itself", "let", "me", "more", "most", "mustn", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan", "she", "should", "shouldn", "so", "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "re", "ve", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn", "we", "were", "weren", "what", "when", "where", "which", "while", "who", "whom", "why", "with", "won", "would", "wouldn", "you", "your", "yours", "yourself", "yourselves"]):
            tokens.remove(token)
    for token in tokens[:]:
        if (len(token) < 4):
            tokens.remove(token)
    global frequencies
    for token in tokens:
        if (token not in frequencies):
            frequencies[token] = 0
        frequencies[token] += 1
    #Helps with page_lengths
    global page_lengths
    page_lengths[resp.url] = len(tokens)
    #Helps with unique_pages
    global unique_pages
    unique_pages += 1
    for page in links:
        unique_pages += 1
    #Helps with subdomains
    global subdomains
    if (".ics.uci.edu/" in resp.url):
        subdomain = resp.url[0:str(resp.url).find(".ics.uci.edu/")]
        if ("http://" in subdomain):
            subdomain = subdomain.replace("http://", "")
        elif ("https://" in subdomain):
            subdomain = subdomain.replace("https://", "")
        if (subdomain not in subdomains):
            subdomains[subdomain] = 0
        subdomains[subdomain] += 1
    '''
    #Removes Query and Beyond
    for i in range(0, len(links)-1):
        if ("?" in links[i]):
            links[i] = links[i][0:links[i].index("?")]
    #Assures No Duplicates of Past Links
    for link in links[:]:
        if (link in visited):
            links.remove(link)
    #Assures No Long Paths
    for link in links[:]:
        if (link.count("/") > 12):
            links.remove(link)
    #Assures No Colons
    for link in links[:]:
        if (link.count(":") > 1):
            links.remove(link)
    #NOT WORKING AS INTENDED: Assures URLs are Not too Similar
    '''
    remove_list = []
    for link in links[:]:
        similarity_threshold = int(len(link) * 0.85)
        for past_link in visited:
            if (link[0:similarity_threshold] == past_link[0:similarity_threshold] and len(link) == len(past_link) and link != past_link):
                remove_list.append(link)
                break

    count = 0
    for link in links[:]:
        similarity_threshold = int(len(link) * 0.85)
        for link2 in links[count:]:
            if (link[0:similarity_threshold] == link2[0:similarity_threshold] and len(link) == len(link2) and link != link2):
                remove_list.append(link2)
        count += 1
        visited.add(link)

    links = set(links)
    links = list(links)
    remove_list = set(remove_list)
    remove_list = list(remove_list)

    print(remove_list)
    
    for link in links[:]:
        if (link in remove_list):
            links.remove(link)
    '''
    #Keeps Track of Number of Pages Crawled
    global crawled
    crawled += 1
    crawled = crawled + len(links)
    
    #Keeps Track of Counters (Uncomment to Test)
    '''
    print("Crawled Pages: " + str(crawled))
    print("Unique Pages: " + str(unique_pages))
    
    freq50 = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)[:50]
    for i in range(0, 50):
        freq50[i] = freq50[i][0]
    print("Top 50 Frequencies: " + str(freq50))
    
    longest_page = sorted(page_lengths.items(), key=lambda x: x[1], reverse=True)[0][0]
    print("Longest Page Length: " + str(longest_page))

    subdomains_list = sorted(subdomains.items(), key=lambda x: x[0])
    print("ICS Subdomains: " + str(subdomains_list))
    '''
    
    return links

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
    except:
        return False
