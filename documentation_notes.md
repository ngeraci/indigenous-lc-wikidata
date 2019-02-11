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

