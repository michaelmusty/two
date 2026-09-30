\\ Actual Makdisi group/lifting cost on a known curve of specified genus.
\\ This curve is NOT the target Y. Default: g=64, a=2, precision 97^4.
default(nbthreads,1);
setrand(20260916);
read("../../pari/.build/lifttors/install.gp");
read("GalRep.gp");
check(ok,message)=if(!ok,error(message));
RRinf(n,g)=concat(vector(n\2+1,j,x^(j-1)),if(n<2*g+1,[],vector((n-2*g-1)\2+1,j,y*x^(j-1))));
{
  if(type(bench_genus)!="t_INT",bench_genus=64);
  if(type(bench_a)!="t_INT",bench_a=2);
  if(type(bench_e)!="t_INT",bench_e=4);
  g=bench_genus; a=bench_a; e=bench_e; p=97; d0=2*g+1;
  f=y^2-(x^(2*g+1)-x);
  check((2*g)%p!=0,"good reduction");
  t0=getwalltime();
  J=PicInit(f,[],g,d0,[RRinf(d0,g),RRinf(2*d0,g),RRinf(3*g+1,g),RRinf(3*g+1,g)],y,p,a,e);
  init_ms=getwalltime()-t0;
  print("STAGE|initialized|genus=",g,"|points=",#J[14],"|ms=",init_ms);
  T=JgetT(J); pe=Jgetpe(J); Z=J[14];
  \\ Q0=(0,0), Q1=(1,0). D=(d0-2)*infinity+Q0+Q1 is effective,
  \\ [D-d0*infinity]=[Q0-Q1] is nonzero 2-torsion. This exact RR
  \\ space supplies an independent known answer for the Hensel lift.
  Wfn=concat(x*(x-1)*vector(g,j,x^(j-1)),[y,x*y]);
  W=matrix(#Z,#Wfn,i,j,Pol(liftall(Mod(Mod(substvec(Wfn[j],[x,y],Z[i]),T),pe)),variable(T)));
  J[1]=0;J[4]=[];J[14]=[];
  J1=PicRed(J,1); W1=liftall(Mod(W,p));
  \\ Membership of this supplied W follows from its displayed exact RR
  \\ basis. The general membership diagnostic is substantially costlier
  \\ than a group operation; do not include it in the operation benchmark.
  check(PicIsZero_val(J1,W1)==0,"known nonzero point");
  t0=getwalltime();
  check(PicIsZero_val(J,PicAdd(J,W,W))==e,"known point doubles to zero");
  double_ms=getwalltime()-t0;
  print("STAGE|doubling_checked|ms=",double_ms);
  t0=getwalltime();
  WL=if(type(bench_original)=="t_INT" && bench_original==1,
    PicLiftTors_original(J,W1,1,2),PicLiftTors(J,W1,1,2));
  lift_ms=getwalltime()-t0;
  print("STAGE|lift_completed|ms=",lift_ms);
  t0=getwalltime();
  check(PicEq_val(J,WL,W)==e,"lift equals independent exact branch divisor");
  check(PicIsZero_val(J,PicMul(J,WL,2,0))==e,"lift is 2-torsion");
  check_ms=getwalltime()-t0;
  print("DATA|{\"genus\":",g,",\"d0\":",d0,",\"p\":",p,",\"a\":",a,
    ",\"precision_exponent\":",e,",\"evaluation_points\":",#Z,
    ",\"section_dimensions\":",vector(3,i,matsize(J[10][i])[2]),
    ",\"jacobian_size_bytes\":",sizebyte(J),
    ",\"timing_ms\":{\"init\":",init_ms,",\"double_and_zero_check\":",double_ms,
    ",\"lift_one_point\":",lift_ms,",\"lift_checks\":",check_ms,"}}");
  print("PASS|101_lifttors_scale");
}
quit;
