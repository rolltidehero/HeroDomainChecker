import gensim.downloader as api
import requests

# Load pre-trained Word2Vec model
w2v_model = api.load("word2vec-google-news-300")

# Target word
target_word = "cybersecurity"

# Get the top 10 most similar words to the target word
similar_words = w2v_model.most_similar(target_word, topn=10)

# Prepare list of domain names to check
domains_to_check = []

for word, similarity in similar_words:
    # Add word ending in "s"
    domain_s = f"{word}s.com"
    domains_to_check.append(domain_s)
    
    # Add word ending in "z"
    domain_z = f"{word}z.com"
    domains_to_check.append(domain_z)
    
    # Add hyphenated version of the word with "s" ending
    domain_hyphen_s = f"{word}s-{target_word}.com"
    domains_to_check.append(domain_hyphen_s)
    
    # Add hyphenated version of the word with "z" ending
    domain_hyphen_z = f"{word}z-{target_word}.com"
    domains_to_check.append(domain_hyphen_z)

# Check availability of domains using DNSimple API
auth_token = "your_dnsimple_api_token"
base_url = "https://api.dnsimple.com/v2"
account_id = "your_dnsimple_account_id"
headers = {"Authorization": f"Bearer {auth_token}", "Accept": "application/json"}

available_domains = []

for domain in domains_to_check:
    domain_url = f"{base_url}/{account_id}/registrar/domains/{domain}/check"
    response = requests.get(domain_url, headers=headers)
    
    if response.status_code == 200:
        availability = response.json()["data"]["available"]
        if availability:
            available_domains.append(domain)

# Print available domains
print("Available domains:")
for domain in available_domains:
    print(domain)
