""" Uses Library of Congress linked data API to recursively
get all narrower terms of a given subject heading URI and
write them to a CSV file called 'narrower_terms.csv'
with columns 'URI', 'Label', and 'Include'.

"""
import re
import csv
from urllib.parse import quote
import requests
import pandas as pd
from bs4 import BeautifulSoup

# a regular expression to match the labels we want
LABEL_RE = re.compile(r'^(?!Older).* Indians( \(.*\))?$')

def main():
    """
    Write CSV headers and call term-getting functions.
    """

    outfile = 'lcsh.csv'
    with open(outfile, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['URI', 'Label'])

    get_narrower_terms_recursive(
        'http://id.loc.gov/authorities/subjects/sh85065184', outfile
    )

    compound_term_uris = get_compound_terms('http://id.loc.gov/authorities/childrensSubjects/sj96005727')
    for uri in compound_term_uris:
        get_narrower_terms_recursive(uri, outfile)


def get_narrower_terms_recursive(subject_uri, outfile):

    rdf = requests.get(subject_uri + '.rdf').text
    soup = BeautifulSoup(rdf, features="html.parser")

    narrower_terms = soup.find_all('madsrdf:hasnarrowerauthority')

    with open(outfile, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for term in narrower_terms:
            authority = term.find('madsrdf:authority')
            uri = authority['rdf:about']
            label = authority.find('madsrdf:authoritativelabel').text
            if re.match(LABEL_RE, label):
                writer.writerow([uri, label])
            get_narrower_terms_recursive(uri, outfile)


def get_compound_terms(subject_uri):
    """ compound subject headings that have the specified subject URI as the first component
        and a geographic term as the second component
    """
    selected_uris = []
    search_urls = get_search_urls(subject_uri)
    complex_subject_uris = uris_from_search_urls(search_urls)

    for uri in complex_subject_uris:
        rdf = requests.get(uri).text
        soup = BeautifulSoup(rdf, features='html.parser')
        components = soup.find("madsrdf:componentlist").find_all(attrs={"rdf:about": True})
        if len(components) == 2:
            if components[0]["rdf:about"] == subject_uri:
                if components[1].name == "madsrdf:geographic":
                    selected_uris.append(uri[:-4])
    return selected_uris


def get_search_urls(subject_uri):
    """ Return list of URLs for search result pages
        for complex subjects that contain the label
        for the given URI.
    """
    rdf = requests.get(subject_uri + ".rdf").text
    label = BeautifulSoup(rdf, features='html.parser').find('madsrdf:authoritativelabel').text
    base_query_url = ('http://id.loc.gov/search/?q=rdftype:ComplexSubject&q=' +
             quote(label) +
            '&format=atom')
    base_request = requests.get(base_query_url).text
    base_query = BeautifulSoup(base_request, features='html.parser')
    total_results = int(base_query.find("opensearch:totalresults").text)
    start_index = int(base_query.find("opensearch:startindex").text)
    items_per_page = int(base_query.find("opensearch:itemsperpage").text)

    search_page_urls = [base_query_url]
    start_item = start_index + items_per_page
    while start_item < total_results:
        url = base_query_url + "&start=" + str(start_item)
        search_page_urls.append(url)
        start_item += items_per_page

    return search_page_urls

def uris_from_search_urls(search_urls):
    """ Takes a list of LC search urls
        Returns list of subject URIs from those search result pages
    """
    complex_subject_uris = []
    for url in search_urls:
        page = BeautifulSoup(requests.get(url).text, features="html.parser")
        for link in page.find_all("link", type="application/rdf+xml"):
            complex_subject_uris.append(link["href"])

    return complex_subject_uris


if __name__ == '__main__':
    main()
