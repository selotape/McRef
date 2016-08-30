# takes in an MS commandline (from file) and generates a seqfile which can be given as input to MCMC.
# gets as parameters a name of a file containing the commandline and the sequence length for simulation.

scriptDir=`readlink -f $0 | sed 's|[^/]*$||'`

ms_cmd_file=$1
seq_len=`cat ${ms_cmd_file} | awk '{if($1=="ms") {print $7;}}'`

ms_dir=$scriptDir;
ms_treefile=ms-trees.txt
seq_file=seqs.txt


ms_cmd=$ms_dir`grep -v "#" $ms_cmd_file | tr "\n" " "`

# echo $ms_cmd
$ms_cmd > $ms_treefile

tail -n+4 $ms_treefile | grep -v // > $ms_treefile.tmp
# with changing genealogies per locus (partitions)
echo 'seq len='$seq_len
$scriptDir/seq-gen -mHKY -l $seq_len -p 1000 <$ms_treefile.tmp  >>$seq_file.seqgen

bash $scriptDir/seqgen-to-gphocs.sh  $seq_file.seqgen $seq_file

rm $seq_file.seqgen $ms_treefile.tmp

