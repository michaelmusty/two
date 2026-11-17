#!/bin/bash
# usage: full3.sh N M0 JOBS ; script 17 on all 3855 records at precision N with
# Newton block M0, in chunks of 32 records, at most JOBS processes at a time
# (starts 30 s apart), then script 18. Restartable: finished chunks are skipped.
# Launch from an exec call with a large --timeout (it becomes the CPU limit).
N=$1; M0=$2; JOBS=$3; cd prec_$N
ln -sf ../17_lift_points_padic.m ../18_power_sums_padic.m .
cat > chunk.sh <<EOF
#!/bin/bash
k=\$1; a=\$2; b=\$3
grep -q "^DONE" s17_\${k}_\$a.out 2>/dev/null && exit 0
flock start.lock sleep 30
PREC=$N M0=$M0 VB=../../pivot_tors/vb_\$k.txt FIRST=\$a LAST=\$b OUT=fx_\${k}_\$a.txt magma -b 17_lift_points_padic.m > s17_\${k}_\$a.out 2>&1
EOF
chmod +x chunk.sh
for k in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
  last=256; [ $k = 15 ] && last=15
  for a in $(seq 1 32 $last); do
    b=$((a+31)); [ $b -gt $last ] && b=$last
    echo "$k $a $b"
  done
done > chunks.txt
xargs -P $JOBS -L 1 ./chunk.sh < chunks.txt
LIST=$(ls fx_*_*.txt | tr '\n' ',' | sed 's/,$//')
PREC=$N LIST=$LIST KMAX=3 magma -b 18_power_sums_padic.m > s18.out 2>&1
echo FULL_DONE >> s18.out
