""" Uses Library of Congress linked data API to recursively
get all narrower terms of a given subject heading URI and
write them to a CSV file called "narrower_terms.csv"
with columns "URI" and "Label".

"""
import csv
import requests
from bs4 import BeautifulSoup


def main():
    """
    Write CSV headers and call term-getting function.
    """

    outfile = "narrower_terms.csv"
    with open(outfile, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URI", "Label"])

    get_narrower_terms_recursive(
        "http://id.loc.gov/authorities/subjects/sh85065184", outfile
    )


def get_narrower_terms_recursive(subject_uri, outfile):

    rdf = requests.get(subject_uri + ".rdf").text
    soup = BeautifulSoup(rdf, "lxml")

    narrower_terms = soup.find_all("madsrdf:hasnarrowerauthority")

    with open(outfile, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for term in narrower_terms:
            authority = term.find("madsrdf:authority")
            uri = authority["rdf:about"]
            label = authority.find("madsrdf:authoritativelabel").text
            writer.writerow([uri, label])
            get_narrower_terms_recursive(uri, outfile)


if __name__ == "__main__":
    main()
