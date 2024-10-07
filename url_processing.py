# Program for different functions to be performed on the URL

import numpy as np
import pandas as pd
import requests
from urllib.parse import urlparse

"""
Shannon Entropy
Given by E = ΣPi * log2(Pi)
where Pi = probability of each character in the URL or domain
"""
def compute_shannon_entropy(url_or_domain):
    if len(url_or_domain) == 0:
        return 0
    char_prob = [float(url_or_domain.count(char))/len(url_or_domain)
                 for char in set(url_or_domain)]
    return -sum([prob * np.log2(prob) for prob in char_prob if prob>0])

def check_for_repeated_digits(url_or_domain_or_sub):
    for char in url_or_domain_or_sub:
        if char.isdigit():
            if url_or_domain_or_sub.count(char) > 1:
                return 1
    return 0

def feature_extractor(url):
    list_features = []

    features = {
        'url_length': len(url),
        'number_of_dots_in_url': url.count('.'),
        'having_repeated_digits_in_url': check_for_repeated_digits(url),
        # If url has a number of characters, check for repeated digits in url
        'number_of_digits_in_url': sum(char.isdigit() for char in url),
        'number_of_special_char_in_url': sum(not char.isalnum() and char.isascii() for char in url),
        # How many ASCII characters that are not alphanumeric
        'number_of_hyphens_in_url': url.count('-'),
        'number_of_underline_in_url': url.count('_'),
        'number_of_slash_in_url': url.count('/'),
        'number_of_questionmark_in_url': url.count('?'),
        'number_of_equal_in_url': url.count('='),
        'number_of_at_in_url': url.count('@'),
        'number_of_dollar_in_url': url.count('$'),
        'number_of_exclamation_in_url': url.count('!'),
        'number_of_hashtag_in_url': url.count('#'),
        'number_of_percent_in_url': url.count('%'),

        # netloc contains NETwork LOCation that includes the domain and subdomain
        'domain_length': len(urlparse(url).netloc),
        'number_of_dots_in_domain': urlparse(url).netloc.count('.'),
        'number_of_hyphens_in_domain': urlparse(url).netloc.count('-'),
        'having_special_characters_in_domain': any(not char.isalnum() and char.isascii() for char in urlparse(url).netloc),
        'number_of_special_characters_in_domain': sum(not char.isalnum() and char.isascii() for char in urlparse(url).netloc),
        'having_digits_in_domain': any(char.isdigit() for char in urlparse(url).netloc),
        'number_of_digits_in_domain': sum(char.isdigit() for char in urlparse(url).netloc),
        'having_repeated_digits_in_domain': check_for_repeated_digits(urlparse(url).netloc),

        'number_of_subdomains': urlparse(url).netloc.count('.') - 1,
        'having_dot_in_subdomain': urlparse(url).netloc.count('.') > 1,
        'having_hyphen_in_subdomain': urlparse(url).netloc.count('-')>0,
        'average_subdomain_length': np.mean([len(subdomain) for subdomain in urlparse(url).netloc.split('.')]),
        'average_number_of_dots_in_subdomain': np.mean([subdomain.count('.') for subdomain in urlparse(url).netloc.split('.')]),
        'average_number_of_hyphens_in_subdomain': np.mean([subdomain.count('-') for subdomain in urlparse(url).netloc.split('.')]),
        'having_special_characters_in_subdomain': any(not char.isalnum() and char.isascii() for char in urlparse(url).netloc.split('.')),
        'number_of_special_characters_in_subdomain': sum(not char.isalnum() and char.isascii() for char in urlparse(url).netloc.split('.')),
        'having_digits_in_subdomain': any(char.isdigit() for char in urlparse(url).netloc.split('.')),
        'number_of_digits_in_subdomain': sum(char.isdigit() for char in urlparse(url).netloc.split('.')),
        'having_repeated_digits_in_subdomain': check_for_repeated_digits(urlparse(url).netloc.split('.')),

        'having_path': len(urlparse(url).path) > 0,
        'path_length': len(urlparse(url).path),
        'having_query': len(urlparse(url).query) > 0,
        'having_fragment': len(urlparse(url).fragment) > 0,
        'having_anchor': url.count('#') > 0,
        'average_subdomain_length': np.mean([len(subdomain) for subdomain in urlparse(url).netloc.split('.')]),
        'entropy_of_url': compute_shannon_entropy(url),
        'entropy_of_domain': compute_shannon_entropy(urlparse(url).netloc)
    }

    for key, value in features.items():
        list_features.append(value)

    # features = np.array(list_features).reshape(1, -1) # 1 column, as many rows as necessary
    features_df = pd.DataFrame([list_features], columns=features.keys())
    return features_df

def url_fetcher():
    url = 'https://openphish.com/feed.txt'
    response = requests.get(url)
    if response.status_code == 200:
        urls = response.text.splitlines()
        return urls
    else:
        print(f'Sorry, URLs could not be fetched. Error: {response.status_code}')
        return []