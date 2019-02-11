import pandas as pd

def main():

	make_wikidata_csv("subject_headings.csv", "lcsh_wikidata.csv")

def make_wikidata_csv(infile, outfile):

	# read csv
	dataframe_1 = pd.read_csv(infile).fillna("")

	# retain only values that don't have Wikidata URIs
	dataframe_1 = dataframe_1[dataframe_1["Wikidata URI"]==""]

	# make new dataframe
	wiki_refine_df = pd.DataFrame()
	wiki_refine_df["LC Identifier"] = dataframe_1["LCSH URI"].str.split("/").str[5]
	wiki_refine_df["Possible Wikidata Label 1"] = dataframe_1["LCSH Label"].str.replace("Indians", "people")
	wiki_refine_df["Possible Wikidata Label 2"] = dataframe_1["LCSH Label"].str.replace("Indians", "")
	wiki_refine_df["LC Label 1"] = dataframe_1["LCSH Label"]

	# split "LCSH Variant Labels" to multiple columns, retain first 5 values
	alt_labels = dataframe_1['LCSH Variant Labels'].apply(lambda x: pd.Series(x.split(';'))).iloc[:,0:5]
	alt_labels.columns = ['LC Label ' + str(col + 2) for col in alt_labels.columns]
	wiki_refine_df = wiki_refine_df.join(alt_labels)
	wiki_refine_df = wiki_refine_df

	# write out
	wiki_refine_df.fillna("").to_csv(outfile, index=False)

if __name__ == "__main__":
	main()