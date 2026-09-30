\\ Compare original and streamed lifting, including both lifting branches,
\\ odd final precision, nontrivial initial precision, and worker threads.
read("../../pari/.build/lifttors/install.gp");
read("GalRep.gp");
check(ok,message)=if(!ok,error(message));
{
  S=read("../../data/computed/lifttors_q8_control.bin");
  if(#S!=6 || #S[1]!=16,S=S[#S]);
  J=S[1]; BL=S[3]; p=Jgetp(J);
  cases=[[2,1],[3,1],[5,1],[7,2],[16,3],[64,1]];
  points=concat([JgetW0(J)],BL); count=0;
  t0=getwalltime();
  for(threads=1,2,
    default(nbthreads,threads);
    for(c=1,#cases,
      e=cases[c][1]; eini=cases[c][2]; Je=PicRed(J,e);
      for(i=1,#points,
        W=liftall(Mod(points[i],p^eini));
        seed=20260917+100*c+i;
        setrand(seed); A=PicLiftTors_original(Je,W,eini,2);
        setrand(seed); B=PicLiftTors(Je,W,eini,2);
        check(PicEq_val(Je,A,B)==e,"original/streamed lift discrepancy");
        check(PicEq_val(Je,B,liftall(Mod(points[i],p^e)))==e,"independent saved lift");
        check(PicMember_val(Je,B)==e,"lift membership");
        check(PicIsTorsion_val(Je,B,2)==e,"lift torsion");
        check(PicEq_val(PicRed(Je,eini),liftall(Mod(B,p^eini)),W)==eini,"reduction");
        count++;
      );
    );
  );
  check(count==60,"all comparison cases");
  print("DATA|{\"comparison_count\":",count,
    ",\"threads\":[1,2],\"final_initial_precisions\":",cases,
    ",\"points_including_origin\":5,\"timing_ms\":",getwalltime()-t0,"}");
  print("PASS|103_lifttors_lift_validation");
}
quit;
