# IRC_to_com
Python script that converts the points of IRC calculations into Gaussian input files (com) with the keywords that the user specifies.

Instructions:

(1) Take the coordinates from an IRC calculations and generate Gaussian input files with the command line that you want.

(2) The program recognizes charge and multiplicity from the parent IRC calculation.

(3) If you need to include text at the end, it's possible using the --gen option (i.e. for calculations with gen, genecp or .wfn generation)

Example reading multiple output files:

python IRC_prep.py *.log --append NAME --route "COMMAND LINE WITHOUT #" --mem 96GB --nproc 24

*** it also works with *.out

*** it works for one or multiple IRC files
