"""

"""
import csv
import re
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
from SPARQLWrapper import SPARQLWrapper, JSON

def main():

    dataset = []

    primary_uri = "http://id.loc.gov/authorities/subjects/sh85065184"
    childrens_uri = "http://id.loc.gov/authorities/childrensSubjects/sj96005727"

    get_narrower_terms_recursive(primary_uri, dataset)

    compound_subject_uris = get_compound_terms(childrens_uri)
    for uri in compound_subject_uris:
        get_narrower_terms_recursive(uri, dataset)

    dataset = tidy(dataset)

    write_out(dataset, "subject_headings.csv")


def get_narrower_terms_recursive(subject_uri, dataset):

    rdf = requests.get(subject_uri + '.rdf').text
    soup = BeautifulSoup(rdf, features="html.parser")
    label_re = re.compile(r'^(?!Older).* Indians( \(.*\))?$')

    narrower_terms = soup.find_all('madsrdf:hasnarrowerauthority')

    for term in narrower_terms:
        authority = term.find('madsrdf:authority')
        lc_uri = authority['rdf:about']
        lc_label = authority.find('madsrdf:authoritativelabel').text

        lc_variants = ";".join([label.text for label in authority.find_all('madsrdf:variantlabel')])
        if re.match(label_re, lc_label):
            lc_variants = get_variant_labels(lc_uri)
            wikidata = get_wikidata(lc_uri)
            dataset.append({"LCSH URI": lc_uri,
                            "LCSH Label": lc_label,
                            "LCSH Variant Labels": ";".join(lc_variants),
                            "Wikidata URI": wikidata["uri"],
                            "Wikidata Label": wikidata["label"]})

        get_narrower_terms_recursive(lc_uri, dataset)

def get_variant_labels(lc_uri):
    """ Take LC URI, return list of variant labels.
    """
    rdf = requests.get(lc_uri + '.rdf').text
    soup = BeautifulSoup(rdf, features="html.parser")
    variant_labels = [label.text for label in soup.find_all("madsrdf:variantlabel")]

    return variant_labels

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


def get_wikidata(lc_uri):

    lc_identifier = lc_uri.split("/")[5]

    # initialize sparql wrapper
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    query_parts = []
    select_where = "SELECT ?item ?itemLabel WHERE {"
    # wdt:P244 is the property for LC Authority URI
    query = '?item wdt:P244 "{}".'.format(lc_identifier)
    language = 'SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }'
    closing = "}"
    for part in [select_where, query, language, closing]:
        query_parts.append(part)
    request = "\n".join(query_parts)
    sparql.setQuery(request)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    wikidata_uri = ";".join([item["item"]["value"] for item in results["results"]["bindings"]])
    wikidata_label = ";".join([item["itemLabel"]["value"] for item in results["results"]["bindings"]])

    return {"uri": wikidata_uri, "label": wikidata_label}

def tidy(dataset):
    """ Remove duplicate rows
        Sort by LCSH Label
    """
    ## https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python
    dataset = [dict(t) for t in {tuple(d.items()) for d in dataset}]

    dataset = sorted(dataset, key=lambda k: k['LCSH Label'])

    return dataset

def write_out(dataset, outfile):
    """ List of dicts to CSV file
    """
    with open(outfile, "w", encoding="utf-8", newline="") as csv_out:
        writer = csv.DictWriter(csv_out, fieldnames=dataset[0].keys())
        writer.writeheader()
        for row in dataset:
            writer.writerow(row)

if __name__ == '__main__':
    main()
