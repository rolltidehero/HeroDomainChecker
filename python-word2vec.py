import logging
import sys
from concurrent.futures import ThreadPoolExecutor
import requests
import json
import time
import re
from itertools import product

# Configure logging
logging.basicConfig(filename='domain_check.log', level=logging.INFO)

# Define the function for checking domain availability
def check_domain(domain, tld):
    url = 'https://api.dnsimple.com/v2/registrar/domains/{}/check'.format(domain + '.' + tld)
    headers = {'Accept': 'application/json', 'Authorization': 'Bearer API_TOKEN'}
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    response_text = response.text

    # Check if the domain is available or not
    available = False
    premium = False
    if status_code == 200:
        result = json.loads(response_text)
        available = result['data'][0]['available']
        premium = result['data'][0]['premium']

    # Log the result
    logging.info('Domain: %s, TLD: %s, Available: %s, Premium: %s', domain, tld, available, premium)

# Define the function for generating domain names
def generate_domains(topic, count, tlds):
    words = w2v_model.most_similar(topic, topn=count)
    domains = []
    for word, similarity in words:
        word = re.sub(r'[^a-z]', '', word.lower())
        if len(word) > 3 and word not in domains:
            domains.append(word)
            domains.append(word + 's')
            domains.append(word + 'z')
            domains.append(word + '-security')
    domain_tlds = list(product(domains, tlds))
    with ThreadPoolExecutor() as executor:
        for domain, tld in domain_tlds:
            executor.submit(check_domain, domain, tld)

# Get user input for topic, count, and TLDs
topic = input("Enter topic: ")
count = int(input("Enter count: "))
tlds = input("Enter TLDs (separated by comma): ").split(',')

# Call the function to generate domains and check availability
generate_domains(topic, count, tlds)
