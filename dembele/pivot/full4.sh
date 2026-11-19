#!/bin/bash
# usage: full4.sh N M0 JOBS ; continuation of full3.sh after an interruption.
# Keeps finished chunks and the complete records of interrupted chunks
# (script 17 appends each record, 8 lines ending with ]>,), and runs the missing records in
# chunks of at most 4 (list chunks4.txt, built once), then script 18.
# Restartable in the same way. Launch from an exec with a large --timeout.
N=$1; M0=$2; JOBS=$3; cd prec_$N
if [ ! -f chunks4.txt ]; then
  while read k a b; do
    f=fx_${k}_$a.txt; s=$a
    if grep -q "^DONE" s17_${k}_$a.out 2>/dev/null; then continue; fi
    if [ -f $f ]; then
      # keep complete record lines only
      awk '/^\/\//{print; next} /^</{buf=""} {buf=buf $0 "\n"} /^\]>,$/{printf "%s", buf; buf=""}' $f > $f.keep; n=$(grep -c "^]>,$" $f.keep)
      mv $f $f.orig; mv $f.keep $f; mv s17_${k}_$a.out s17_${k}_$a.out.partial
      s=$((a+n))
    fi
    while [ $s -le $b ]; do e=$((s+3)); [ $e -gt $b ] && e=$b; echo "$k $s $e"; s=$((e+1)); done
  done < chunks.txt > chunks4.txt
fi
xargs -P $JOBS -L 1 ./chunk.sh < chunks4.txt
LIST=$(ls fx_*_*.txt | tr '\n' ',' | sed 's/,$//')
PREC=$N LIST=$LIST KMAX=3 magma -b 18_power_sums_padic.m > s18.out 2>&1
echo FULL_DONE >> s18.out
