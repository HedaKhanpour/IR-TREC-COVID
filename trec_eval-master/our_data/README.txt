The trec_eval-master folder should contain everything we need to evaluate our 
ranking.

Only the sub-folder 'our_data' and its contents was added by me, the
rest came from https://github.com/usnistgov/trec_eval. (Technically I also added
'cygwin1.dll', as I'm using Windows I was required to install Cygwin and add
this file to make this work).

The folder 'our_data' contains the file 'CRJ.txt' which contains all the 
available relevance judgements for our data. Files 'TR1', 'TR2' and 'TR3' are
tiny test rankings that I made to see how the trec evaluation tool works.

I have been able to use the tool by using the Cygwin command line in the
trec_eval-master directory (I suspect the Linux command line would work as well).
Here are some example commands:
	run trec_eval -M3 our_data/CRJ.txt our_data/TR2.txt
	run trec_eval -q -M1000 our_data/CRJ.txt our_data/TR2.txt
	run trec_eval -q -M1000 -m official our_data/CRJ.txt our_data/TR2.txt
	run trec_eval -q -M1000 -m set our_data/CRJ.txt our_data/TR2.txt
Here:
	'-MX' determines the maximum number X of articles included in the ranking.
	'our_data/CRJ.txt' is the file containing the relevance judgements
	'our_data/TR2.txt' is the file containing our rankings
	'-q' causes it to show results for each individual topic as well
	'-m' followed by 'official'/'set'/... determines which measures are used
There are other parameters as well, more information can be found in the 
comments at the start of 'trec_eval.c'.

Information about (amongst other things) the ranking file format: https://ir.nist.gov/covidSubmit/round5.html
Information about the 50 topics: https://ir.nist.gov/covidSubmit/data/topics-rnd5.xml