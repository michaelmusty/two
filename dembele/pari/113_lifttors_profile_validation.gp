\\ Diagnostic hooks must preserve exact outputs and random-state evolution.
default(nbthreads,1);
read("../../pari/.build/lifttors_profile/install.gp");
read("GalRep.gp");
check(ok,message)=if(!ok,error(message));
{
  S=read("../../data/computed/lifttors_q8_control.bin");
  if(#S!=6 || #S[1]!=16,S=S[#S]);
  J=S[1];p=Jgetp(J);points=concat([JgetW0(J)],S[3]);
  cases=[[2,1],[5,1],[7,2],[64,1]];count=0;
  for(k=1,#cases,
    e=cases[k][1];eini=cases[k][2];Je=PicRed(J,e);
    for(i=1,#points,
      W=liftall(Mod(points[i],p^eini));seed=20260918+100*k+i;
      LiftProfileEnable(0);setrand(seed);A=PicLiftTors(Je,W,eini,2);stateA=getrand();
      LiftProfileEnable(1);setrand(seed);B=PicLiftTors(Je,W,eini,2);stateB=getrand();
      LiftProfileEnable(0);
      check(A==B,"profiling preserves exact matrix representatives");
      check(stateA==stateB,"profiling preserves random-state evolution");
      check(PicEq_val(Je,B,liftall(Mod(points[i],p^e)))==e,"independently saved point");
      check(PicIsTorsion_val(Je,B,2)==e,"torsion after profiling");
      count++;
    );
  );
  check(count==20,"all diagnostic comparison cases");
  print("DATA|{\"comparison_count\":",count,",\"exact_matrices_and_random_states_equal\":true,\"final_initial_precisions\":",cases,"}");
  print("PASS|113_lifttors_profile_validation");
}
quit;
