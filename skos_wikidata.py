#!/usr/bin/env python

import sys

from rdflib import Graph, Namespace
from wikidata_suggest import suggest, Quit

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
WIKIDATA = Namespace("http://www.wikidata.org/entity/")

def match(rdf_filename):
    G = Graph()
    G.parse(rdf_filename)
    q = """
        SELECT ?concept ?label ?close ?exact ?broad ?narrow ?related
        WHERE {
            ?concept a skos:Concept .
            ?concept skos:prefLabel ?label .
            OPTIONAL {
                ?concept skos:closeMatch ?close .
                ?concept skos:exactMatch ?exact .
                ?concept skos:broadMatch ?broad .
                ?concept skos:narrowMatch ?narrow .
                ?concept skos:relatedMatch ?related .
            }
        }
        """

    count = 0
    for concept_uri, label, c, e, b, n, r in G.query(q, initNs={"skos": SKOS}): 
        
        # no need to map again
        if c or e or b or n or r:
            print 'xxx', c, e, b, n, r
            continue
        else:
            print c, e, b, n, r
            continue

        # get our wikidata suggestion
        try:
            wd = suggest(label)
        except Quit:
            print
            print "Thanks for playing: you matched %s concepts" % count
            print
            break

        # if we got a suggestion ask what skos relation to use to link them up
        # and save the new assertion to our file
        if wd:
            rel = pick_rel(label, wd['label'])
            wikidata_uri = WIKIDATA[wd['id']]
            G.add((concept_uri, rel, wikidata_uri))
            G.serialize(open(rdf_filename, "w"))
            count += 1


def pick_rel(l1, l2):
    rel = None
    while rel == None:
        print
        print("Is %s an e)xact, c)lose, b)roader, n)arrower, or r)elated match to %s?" % (l1, l2)).encode('utf8'),
        choice = raw_input().lower()[0]
        if choice == "e":
            rel = SKOS.exactMatch
        elif choice == "b":
            rel = SKOS.broadMatch
        elif choice == "n":
            rel = SKOS.narrowMatch
        elif choice == "r":
            rel = SKOS.relatedMatch
    return rel


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: skos_wikidata.py file.rdf"
    else:
        filename = sys.argv[1]
        match(filename)

