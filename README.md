# skos_wikidata

An experimental command line tool for interactively matching SKOS concepts
to Wikidata.

    % pip install -r requirements.txt
    % ./skos_wikidata.py example/uat.rdf

This will look for concepts in your RDF file and ask you to match them up
against Wikidata entities. As assertions are added to the graph they will be 
serialized back to the RDF file. So you can quit at any time and have your work
saved.

By default `skos:exactMatch` assertions will be created between your SKOS
concepts and Wikidata. If you would like to be more nuanced and to also use
`skos:closeMatch`, `skos:broadMatch`, `skos:narrowMatch` and `skos:relatedMatch`
you will will want to:

    % ./skos_wikidata.py --relations-prompt example/uat.rdf 

Also your SKOS may use SKOSXL for labels, in which case you'll need to tell
skos_wikidata.py to query the data a bit differently:

    % ./skos_wikidata.py --skosxl example/uat.rdf 

Because it load the entire concept scheme into memory and writes it back to disk
after every mapping assertion it may not be practical for super large SKOS 
concept schemes. But for thousands of concepts it's not so bad. YMMV. 
Optimizations could be made (not saving all the time, etc) so give it 
a try and let me know!
