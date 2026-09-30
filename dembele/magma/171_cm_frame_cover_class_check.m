// D78: bounded actual divisor-class operations on the genus-40 candidate.
SetQuitOnError(true); SetColumns(0); SetSeed(78);
started:=Cputime();
load "dembele/magma/170_cm_frame_cover_class_arithmetic.m";
ok:=EqualClass(WP,WM); assert not ok;
ok:=ZeroClass(V1); assert ok;
print "PASS|BRANCH_CLASSES_DISTINCT";
// Chord(-WP,WM)=WP-WM with the convention [D-D0].
D:=ChordClass(NegClass(WP),WM);
ok:=ZeroClass(D); assert not ok;
ok:=EqualClass(FrobeniusClass(D),D); assert ok;
minusD:=NegClass(D);
ok:=EqualClass(DeckClass(D),minusD); assert ok;
ok:=ZeroClass(AddClass(D,minusD)); assert ok;
print "PASS|NONZERO_RATIONAL_ANTIINVARIANT_CLASS";
twiceD:=ChordClass(minusD,minusD);
tripleD:=AddClass(twiceD,D);
ok:=ZeroClass(tripleD);
printf "DELTA_KILLED_BY_THREE|%o\n",ok;
printf "DELTA_SECTION_ROWS|%o\n",EncRows(D);
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|171_CM_FRAME_COVER_CLASS_CHECK";
quit;
