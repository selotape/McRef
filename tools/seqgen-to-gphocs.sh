# takes in a seqgen output file and converts it to an G-PhoCS data file.

# usage: bash ./seqgen-to-gphocs.sh <seqgen_output_file> <gphocs_data_file>


seqgenFile=$1
gphocsFile=$2

cat $seqgenFile | \
awk \
'BEGIN{locus=0;lineCount=0;nextLine=0;}\
{\
	if(NF>0) {\
		if(lineCount>=nextLine) {locus=locus+1;         print "\nlocus"locus" "$0; lineCount=0; nextLine=$1}\
		else                    {lineCount=lineCount+1; print;}\
	}\
}\
END{print locus;}'\
> $gphocsFile.tmp

tail -n1 $gphocsFile.tmp > $gphocsFile
head -n-1 $gphocsFile.tmp >> $gphocsFile

rm $gphocsFile.tmp
