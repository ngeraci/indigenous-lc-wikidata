import csv
from SPARQLWrapper import SPARQLWrapper, JSON

def main():

    infile = 'lcsh.csv'

    with open(infile, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        terms = [row for row in reader if row['Include'] == 'True']

    for term in terms:
        # get just the last segment of URI
        identifier = term["URI"].split("/")[5]
        uri = wikidata_uri(identifier)

def wikidata_uri(lc_identifier):

    # initialize sparql wrapper
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    # wdt:P244 is the property for LC Authority URI
    sparql.setQuery('SELECT * WHERE {?item wdt:P244 "' + lc_identifier + '"}')

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for item in results["results"]["bindings"]:
        print(item["item"]["value"])
        sys.stdout.flush()


if __name__ == '__main__':
    main()
