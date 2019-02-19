# indigenous/LC/Wikidata project

These are scripts used in a project to reconcile Library of Congress Subject Heading (LCSH) terms that name indigenous peoples of North America with Wikidata items. The [file](https://github.com/ngeraci/indigenous-lc-wikidata/blob/master/data/lcsh_wikidata.csv) generated by [make_wikidata_csv.py](https://github.com/ngeraci/indigenous-lc-wikidata/blob/master/make_wikidata_csv.py) was used in OpenRefine to match items and upload Library of Congress IDs to Wikidata.

## The problem
[LCSH](https://commons.pacificu.edu/libfac/6/) [is](https://harvest.usask.ca/handle/10388/383) [widely](https://www.tandfonline.com/doi/abs/10.1080/01639374.2017.1382641?journalCode=wccq20) [acknowledged](https://www.tandfonline.com/doi/abs/10.1080/01639374.2015.1010113?casa_token=fi3nnxjroSQAAAAA:V_S7Zbjauo3MDanEFDIhf-RiJs52EN0mzMdIoa3RUveLk0_2xsqXrRq2CYQPOwmOf895p5jq_K3sZQ]) as often being inaccurate, biased or offensive in this area. Most subject headings that are names of tribes and peoples end with the word "Indians" (i.e. "Yaqui Indians," "Cherokee Indians"). Additionally, many of the names themselves don't match current usage, often being drawn from dated anthropological texts (like "Kamia" instead of "Kumeyaay"). In addition to being offensive, these issues create information retrieval problems.

Wikidata, while not perfect, usually uses labels that reflect Wikipedia article titles, which have often been negotiated over time via public discussion. Anecdotally, it appears more likely to match current usage, though it doesn't always reflect self-preferred names of tribes. If you're working on a focused project or collection with a particular community, Wikidata is no substitute for just talking with the people you're working with. But it appears to have potential as a tool to make general digital collections metadata a little less bad.

When a Wikidata item has a Library of Congress ID in [Wikidata property P244](https://www.wikidata.org/wiki/Property:P244), we can more easily get the matching Wikidata item for an LC heading and evaluate whether the Wikidata label may be more appropriate for use in metadata.

## Context
I'm a white metadata librarian living and working on Luiseño, Cahuilla and Tongva land (the Inland Empire of Southern California). I think white librarians should be more proactive in cleaning up the racist messes our professional forebearers made, and this is an experimental effort in that direction.  

## Steps
1. Use LC Linked Data service to get tribe names:
	* Narrower terms of "Indians of North America"
	* Narrower terms of complex subjects that have "Indians of North America"
	as the first term and a geographic subject as the second term.
		* weirdly, complex terms use LC Children's subject URI for same term
	* Use regular expression to match pattern "____ Indians"
	* Total = 500 terms

2. For each name, query Wikidata (part of same script as above):
	* Get Wikidata item if has matching LC identifier
	* Only 26/500 existing matches
		* this means that only 26 Wikidata items already linked to LC, not that other matches don't exist

3. Use OpenRefine to make more matches and add LC identifiers to Wikidata
	* [Tutorial](https://www.wikidata.org/wiki/Wikidata:Tools/OpenRefine/Editing/Tutorials/Video)
	* 360 matched, 114 unmatched (reasons: couldn't verify match,
	no Wikidata item, name in LC refers to a place, a family of languages, or something else other than a group of people)
	* noted 3 instances of vandalism

## Next steps
* Further evaluate unmatched terms
* Improve quality of Wikidata items
* How many headings are different? how many are different not just in "people" vs "Indians", but the primary name used?