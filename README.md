# skos_wikidata

An experimental command line tool for interactively matching SKOS concepts
to Wikidata.

    % pip install -r requirements.txt
    % ./skos_wikidata.py example/uat.rdf

This will look for concepts in your RDF file and ask you to match them up
against Wikidata entities. As assertions are added to the graph they will
be serialized back to the RDF file.

This may not be practical for super large SKOS concept schemes. But for
smaller ones it might not be so bad? Give it a try and let me know.
