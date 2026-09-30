\\ D78: actual genus-40 branch-class arithmetic; no class-number assumption.
default(nbthreads,1);
setrand(20260921);
read("dembele/pari/.build/lifttors_reduction/install.gp");
read("dembele/data/computed/cm_frame_cover_makdisi.gp");
check(ok,message)=if(!ok,error(message));
{
  t0=getwalltime();
  T=cover_T; p=31; e=1; pe=31;
  V=[cover_v1_evaluations,cover_v2_evaluations,cover_v3_evaluations];
  check(vector(3,i,matsize(V[i])[2])==[81,201,321],"section dimensions");
  KV=apply(M->mateqnpadic(M,T,pe,p,e),V);
  ft=lift(lift(Mod(t,Mod(T,p))^p));
  fm=[1,polcoef(ft,0);0,polcoef(ft,1)];
  J=[0,40,120,[],T,p,e,pe,fm,V,KV,V[1],[],[],
     cover_evaluation_frobenius,[cover_evaluation_involution]];
  WP=cover_plus_evaluations; WM=cover_minus_evaluations;
  check(PicMember_val(J,WP)==1 && PicMember_val(J,WM)==1,"branch divisor membership");
  check(PicEq_val(J,WP,WM)==0,"nonprincipal difference");
  print("PASS|BRANCH_REPRESENTATIVES ",getwalltime()-t0);
  D=PicLC(J,[1,-1]~,[WP,WM]);
  check(PicMember_val(J,D)==1 && PicIsZero_val(J,D)==0,"nonzero Delta");
  check(PicEq_val(J,PicFrob(J,D),D)==1,"Delta rational over F31");
  check(PicIsZero_val(J,PicAdd(J,PicAut(J,D,1),D))==1,"Delta anti-invariant");
  triple=PicMul(J,D,3,2);
  print("DELTA_KILLED_BY_THREE|",PicIsZero_val(J,triple));
  writebin("dembele/data/computed/cm_frame_cover_class.bin",[J,D]);
  print("PASS|169_CM_FRAME_COVER_CLASS ",getwalltime()-t0);
}
quit;
