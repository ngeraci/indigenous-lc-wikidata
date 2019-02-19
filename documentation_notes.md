Root of idea: We know LC is inaccurate. Aside from use of "Indians" in names, many of the authorized terms don't match what is currently used (or what has ever been in wide use). Poses information retrieval problem (i.e. Kamia/Kumeyaay). Wikidata, while not perfect, typically uses labels that reflect Wikipedia article titles, which have often been chosen or changed over time via community discussion. More likely to match current use, seems like a good source for general purpose library metadata (and have used it sometimes informally as a reference when an LC name seems very off).

Note that it doesn't always reflect self-preferred names and if you're working on a focused project or collection w a particular community, may not be the best source. I'm approaching it more as a wide-reaching tool to make general digital collections metadata a little less worse.

1. Use LC Linked Data service to get tribe names:
	* Narrower terms of "Indians of North America"
	* Narrower terms of complex subjects that have "Indians of North America"
	as the first term and a geographic subject as the second term.
		* weirdly, complex terms use lc children's subject URI for same term
	* Use regular expression to match pattern "____ Indians"
		* This excludes some Alaska Native and Canadian First Nations peoples,
		was ok with that for scope of this project
	* Total = 500 terms

2. For each name, query Wikidata (part of same script as above):
	* Get Wikidata item if has matching LC identifier
	* Only 26/500 existing matches
		* this means that only 26 Wikidata items already link to LC,
		not that other matches don't exist

3. Use OpenRefine to make more matches and add LC identifiers to Wikidata
	* https://www.wikidata.org/wiki/Wikidata:Tools/OpenRefine/Editing/Tutorials/Video

	* 360 matched, 114 unmatched (reasons: couldn't verify match,
	no Wikidata item, name in LC refers to a place, a family of languages, or something else other than a group of people)

	* noted 3 instances of vandalism

Use case:
	- You've used LCSH headings in the past and have their URIs stored. Now you can write a script that gets the Wikidata item that has that LC identifier, and use it to evaluate where using a label from Wikidata is more appropriate.

Next steps:
	* further evaluate unmatched terms
	* improve quality of Wikidata items
	* how many headings are different? how many are different not just in "people" vs "Indians", but the primary word used?