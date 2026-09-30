\\ Compare the batched exact validator with the retained upstream code.
read("../../pari/.build/lifttors/install.gp");
install("DivSub_dimval","uGGLGGGLG","BoundedVal",lifttors_library);
install("DivSub_dimval_original","uGGLGGGLG","OriginalVal",lifttors_library);
check(ok,message)=if(!ok,error(message));
{
  S=read("../../data/computed/lifttors_q8_control.bin");
  \\ GP writebin appends; read returns all records if run repeatedly.
  if(#S!=6 || #S[1]!=16,S=S[#S]);
  J=S[1];BL=S[3];T=JgetT(J);p=Jgetp(J);e=Jgete(J);pe=Jgetpe(J);
  V=J[10][1];KV=J[11][1];count=0;
  candidates=concat([JgetW0(J)],BL);
  for(k=0,5,
    W=JgetW0(J);W[1,1]+=p^k;
    candidates=concat(candidates,[W]);
  );
  for(i=1,#candidates,
    W=candidates[i];
    a=OriginalVal(V,W,1,KV,T,p,e,pe);
    b=BoundedVal(V,W,1,KV,T,p,e,pe);
    check(a==b,"zero-test discrepancy");count++;
    if(i==1,check(a==e,"origin"));
    if(i>=2 && i<=5,check(a==0,"nonzero torsion"));
    if(i>=6,check(a==i-6,"tamper valuation"));
  );
  for(i=1,5,for(j=1,#candidates,
    WA=candidates[i];WB=candidates[j];
    SWB=matrix(matsize(WB)[1],matsize(WB)[2],r,c,Pol(liftall(Mod(Mod(WA[r,1]*WB[r,c],T),pe)),variable(T)));
    a=OriginalVal(WA,SWB,1,J[11][2],T,p,e,pe);
    b=BoundedVal(WA,SWB,1,J[11][2],T,p,e,pe);
    check(a==b,"equivalence-test discrepancy");count++;
  ));
  \\ Wrong requested dimension must be rejected by both implementations.
  for(dim=2,5,
    check(OriginalVal(V,candidates[1],dim,KV,T,p,e,pe)==0,"original wrong dimension");
    check(BoundedVal(V,candidates[1],dim,KV,T,p,e,pe)==0,"batched wrong dimension");count++;
  );
  print("DATA|{\"comparison_count\":",count,",\"tamper_valuations\":[0,1,2,3,4,5]}");
  print("PASS|102_lifttors_validation");
}
quit;
