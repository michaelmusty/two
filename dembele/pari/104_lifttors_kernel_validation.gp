\\ Compare batched kernels on tall systems with prescribed kernels.
\\ The first 512 rows vanish, so later row batches must affect the result.
read("../../pari/.build/lifttors/install.gp");
check(ok,message)=if(!ok,error(message));
setrand(20260916);
{
  p=7; T=ffinit(p,2,'t); u=ffgen(T,'u); T=lift(T);
  m=787; n=17; count=0; rejected=0; t0=getwalltime();
  for(eindex=1,3,
    e=[1,2,5][eindex];pe=p^e;
    for(rindex=1,4,
      r=[0,1,9,17][rindex];
      C=matrix(r,n,i,j,if(j<=r,i==j,random(pe)+t*random(pe)));
      B=matrix(m,r,i,j,if(i<=512,0,if(i<=512+r,i-512==j,random(pe)+t*random(pe))));
      A=if(r==0,matrix(m,n),liftall(Mod(Mod(B*C,T),pe)));
      \\ The upstream p-adic C routines require polynomial representatives,
      \\ including constant entries (the Jacobian interface uses these too).
      A=matrix(m,n,i,j,Pol(A[i,j],t));
      K=LiftMatker_batched(A,T,pe,p,e);
      check(matsize(K)[2]==n-r,"known nullity");
      if(r<n,
        check(valuation(liftall(Mod(A*K,T)),p)>=e,"all equations at full precision");
        check(matrank(matrix(n,n-r,i,j,subst(K[i,j],t,u)*u^0))==n-r,"free kernel basis");
      );
      if(r>0,
        K0=matkerpadic(A,T,pe,p,e);
        Q=matconcat([K,K0]);
        check(matrank(matrix(n,2*(n-r),i,j,subst(Q[i,j],t,u)*u^0))==n-r,"original kernel span");
      );
      count++;
      if(e>1 && r<n,
        A[1,r+1]=Pol(p,t);
        failed=0;
        iferr(LiftMatker_batched(A,T,pe,p,e),E,
          check(Str(E)=="error(\"Lifting linear system does not have good reduction.\")","expected good-reduction rejection");
          failed=1;
        );
        check(failed,"rank drop modulo p must be rejected");rejected++;
      );
    );
  );
  check(count==12 && rejected==6,"all kernel cases");
  print("DATA|{\"known_kernel_cases\":",count,",\"rank_drop_rejections\":",rejected,
    ",\"rows\":",m,",\"columns\":",n,",\"initial_zero_rows\":512,\"timing_ms\":",getwalltime()-t0,"}");
  print("PASS|104_lifttors_kernel_validation");
}
quit;
