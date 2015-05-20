#!/usr/bin/env python

import sys
import argparse

from rdflib import Graph, Namespace
from wikidata_suggest import suggest, Quit

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
SKOSXL = Namespace("http://www.w3.org/2008/05/skos-xl#")
WIKIDATA = Namespace("http://www.wikidata.org/entity/")
NS = {"skos": SKOS, "skosxl": SKOSXL} 


def match(rdf_filename, relations_prompt=False, skosxl=False):
    G = Graph()
    G.parse(rdf_filename)
    q = query(skosxl)

    count = 0
    for concept_uri, label, c, e, b, n, r in G.query(q, initNs=NS):
        
        # no need to map again
        if c or e or b or n or r:
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
            if relations_prompt:
                rel = pick_rel(label, wd['label'])
            else:
                rel = SKOS.exactMatch
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
        elif choice == "c":
            rel = SKOS.closeMatch
        elif choice == "b":
            rel = SKOS.broadMatch
        elif choice == "n":
            rel = SKOS.narrowMatch
        elif choice == "r":
            rel = SKOS.relatedMatch
    return rel


def query(skosxl):

    # if skosxl is being used we need to look up the labels
    # slightly differently than in vanilla skos

    if skosxl:
        label_query = \
            """
            ?concept skosxl:prefLabel ?labelResource .
            ?labelResource skosxl:literalForm ?label .
            """
    else:
        label_query = """?concept skos:prefLabel ?label ."""

    q = """
        SELECT ?concept ?label ?close ?exact ?broad ?narrow ?related
        WHERE {
            ?concept a skos:Concept .
            %s
            OPTIONAL { ?concept skos:closeMatch ?close . }
            OPTIONAL { ?concept skos:exactMatch ?exact . }
            OPTIONAL { ?concept skos:broadMatch ?broad . }
            OPTIONAL { ?concept skos:narrowMatch ?narrow. }
            OPTIONAL { ?concept skos:relatedMatch ?related . }
        }
        """ % label_query

    return q


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="add Wikidata links to your SKOS")
    parser.add_argument("filename", type=str, help="path to your SKOS RDF")
    parser.add_argument("--relations-prompt", dest="relations_prompt", action="store_true", default=False, help="prompt for the type of SKOS mapping relation to use, otherwise skos:exactMatch will be used")
    parser.add_argument("--skosxl", dest="skosxl", action="store_true", default=False, help="use SKOSXL namespace for labels instead of SKOS")
    args = parser.parse_args()
    match(args.filename, args.relations_prompt, args.skosxl)
