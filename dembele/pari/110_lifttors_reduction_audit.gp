\\ D66: inspect reduction of nested auxiliary evaluation tables.
\\ Read-only audit on the saved Q8 object; never evaluate malformed tables.
default(nbthreads,1);
read("../../pari/.build/lifttors_rows/install.gp");
check(ok,message)=if(!ok,error(message));
{
  S=read("../../data/computed/lifttors_q8_control.bin");
  if(#S!=6 || #S[1]!=16,S=S[#S]);
  J=S[1];p=Jgetp(J);records=List(); failures=0;
  check(type(J[13][1])=="t_VEC" && type(J[13][2])=="t_VEC","auxiliary embedding vectors");
  for(k=1,5,
    e=[1,2,8,32,64][k];q=p^e;Je=PicRed(J,e);
    check(Je[10]==liftall(Mod(J[10],q)),"section evaluations reduce correctly");
    check(Je[11]==liftall(Mod(J[11],q)),"section equations reduce correctly");
    ok=vector(2,i,Je[13][i]==liftall(Mod(J[13][i],q)));
    failures+=2-vecsum(ok);
    listput(records,Str("{\"precision_exponent\":",e,
      ",\"original_auxiliary_types\":[\"",type(J[13][1]),"\",\"",type(J[13][2]),
      "\"],\"reduced_auxiliary_types\":[\"",type(Je[13][1]),"\",\"",type(Je[13][2]),
      "\"],\"auxiliary_tables_match_correct_reduction\":",ok,"}"));
  );
  print("DATA|{\"genus\":2,\"p\":",p,",\"a\":2,\"auxiliary_table_failures\":",failures,
    ",\"section_tables_match_correct_reduction\":true,\"records\":[",
    records[1],",",records[2],",",records[3],",",records[4],",",records[5],"]}");
  print("PASS|110_lifttors_reduction_audit");
}
quit;
