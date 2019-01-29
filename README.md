An exploration of using labels from Wikidata to replace Library of Congress Subject Heading terms that name indigenous peoples in descriptive metadata. 

1. Use Library of Congress linked data API to recursively get all narrower terms for "Indians of North America" and write to CSV file ("narrower_terms.csv"). Use a regular expression to mark labels for inclusion that contain the word "Indians" and refer to overarching groups of people. (get_lc_terms.py)

[include a note about not dealing with "Eskimo" term due to taxonomy issues, not dealing with sub-terms like "Older Navajo Indians", not dealing with terms like "Pima baskets", which is an NT of "Baskets--Arizona"]

TODO: This is missing a bunch! For example, not catching narrower terms of complex subjects like "Indians of North America--California". Need to also get all compound terms that have "Indians of North America" as a component. OOF


2. Manually review CSV file.

3. Get Wikidata URIs based on LC URI