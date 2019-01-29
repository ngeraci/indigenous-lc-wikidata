""" Uses Library of Congress linked data API to recursively
get all narrower terms of a given subject heading URI and
write them to a CSV file called 'narrower_terms.csv'
with columns 'URI', 'Label', and 'Include'.

"""
import re
import csv
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

# a regular expression to match the labels we want
LABEL_RE = re.compile(r'^(?!Older).* Indians( \(.*\))?$')

def main():
    """
    Write CSV headers and call term-getting function.
    """

    # outfile = 'narrower_terms.csv'
    # with open(outfile, 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['URI', 'Label', 'Include'])

    # get_narrower_terms_recursive(
    #     'http://id.loc.gov/authorities/subjects/sh85065184', outfile
    # )

    get_compound_terms('http://id.loc.gov/authorities/subjects/sh85065184')

def get_narrower_terms_recursive(subject_uri, outfile):

    rdf = requests.get(subject_uri + '.rdf').text
    soup = BeautifulSoup(rdf, 'lxml')

    narrower_terms = soup.find_all('madsrdf:hasnarrowerauthority')

    with open(outfile, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for term in narrower_terms:
            authority = term.find('madsrdf:authority')
            uri = authority['rdf:about']
            label = authority.find('madsrdf:authoritativelabel').text
            if re.match(LABEL_RE, label):
                include = 'True'
            else:
                include = 'False'
            writer.writerow([uri, label, include])
            get_narrower_terms_recursive(uri, outfile)


def get_compound_terms(subject_uri):
    """ compound subject headings that have the
    specified subject URI as a component.
    """
    class Search:
        def __init__(self, uri):
            self.uri = uri
            self.rdf = requests.get(self.uri + ".rdf").text
            self.label = BeautifulSoup(self.rdf, features='html.parser'
                                       ).find('madsrdf:authoritativelabel').text
            self.query = ('http://id.loc.gov/search/?q=rdftype:ComplexSubject&q=' +
                          quote(self.label) +
                          '&format=atom')
            self.result_uris = []

        def get_paginated_uris(self):
            results = BeautifulSoup(requests.get(self.query).text,
                                    features='html.parser')
            for a in results.find_all("link", type="application/rdf+xml"):
                self.result_uris.append(a["href"])
            next_page = results.find("link", rel="next")["href"]
            if next_page:
                get_paginated_uris(next_page)

    lc_search = Search(subject_uri)
    get_paginated_uris(lc_search.query)
    print(lc_search.result_uris)


if __name__ == '__main__':
    main()
