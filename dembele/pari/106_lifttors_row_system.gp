\\ D64: measure actual equation storage and verify a row-wise formula.
\\ Uses the unchanged D63 library on known curves; this is a prototype,
\\ not a replacement for its production C lifting routine.
default(nbthreads,1);
setrand(20260916);
read("../../pari/.build/lifttors/install.gp");
install("FqM_mul","GGGG","EMul",lifttors_library);
install("FqM_FqC_mul","GGGG","EMulCol",lifttors_library);
install("FqM_indexrank","GGG","EIndex",lifttors_library);
install("FqM_image","GGG","EImage",lifttors_library);
install("DivMul","GGGG","EDiag",lifttors_library);
install("FqM_MinorCompl","GGG","EMinor",lifttors_library);
install("M2ABCD","GG","ESplit",lifttors_library);
install("mat2col","G","EFlatten",lifttors_library);
check(ok,message)=if(!ok,error(message));
RRinf(n,g)=concat(vector(n\2+1,j,x^(j-1)),if(n<2*g+1,[],vector((n-2*g-1)\2+1,j,y*x^(j-1))));
Ered(M,T,q)=matrix(matsize(M)[1],#M,i,j,Pol(liftall(Mod(Mod(M[i,j],T),q)),variable(T)));
Erows(M,indices)=matrix(#indices,#M,i,j,M[indices[i],j]);
Ecol(M,j,indices)=vector(#indices,k,M[indices[k],j])~;
RowBlock(k,H,S,C,Ip,Ic,rho,T,q)=
{
  my(B=vector(2));
  for(i=1,2,
    B[i]=Ered(EDiag(Ecol(H[i],k,Ic),Erows(S,Ic),T,q)
      -EMul(C,EDiag(Ecol(H[i],k,Ip),Erows(S,Ip),T,q),T,q),T,q);
  );
  matconcat([B[1],B[2],rho[,k]]);
};
{
  if(type(bench_a)!="t_INT",bench_a=51);
  g=4; a=bench_a; p=97; e=4; d0=2*g+1;
  J=PicInit(y^2-(x^(2*g+1)-x),[],g,d0,
    [RRinf(d0,g),RRinf(2*d0,g),RRinf(3*g+1,g),RRinf(3*g+1,g)],y,p,a,e);
  T=JgetT(J);pe=Jgetpe(J);Z=J[14];V=J[10][2];nZ=#Z;nV=#V;
  check(poldegree(T)==a && polisirreducible(Mod(T,p)),"actual unramified field degree");
  visited=vector(nZ);cycles=List();
  for(i=1,nZ,if(!visited[i],j=i;n=0;while(!visited[j],visited[j]=1;n++;j=J[15][j]);listput(cycles,n)));
  check(vecsum(Vec(cycles))==nZ,"Frobenius cycles cover evaluation points");
  Wfn=concat(x*(x-1)*vector(g,j,x^(j-1)),[y,x*y]);
  W=matrix(nZ,#Wfn,i,j,Pol(liftall(Mod(Mod(substvec(Wfn[j],[x,y],Z[i]),T),pe)),variable(T)));
  sw=EIndex(W,T,p)[1];
  U0=matkerpadic(Erows(V,sw),T,p^2,p,2);
  check(#U0==d0,"normalization tangent coordinates");
  results=List(); alpha=ffgen(Mod(T,p),'u);
  for(eini=1,2,
    q=p^eini;q2=q^2;t0=getwalltime();
    U=PicDeflate_U(PicRed(J,eini),Ered(W,T,q),2);
    GWV=matconcat(vector(2,i,EDiag(EMulCol(V,U[,i],T,q2),V,T,q2)));
    uv=EMinor(GWV,T,p);ABCD=ESplit(GWV,uv);
    Ip=uv[1][1];Ic=uv[1][2];P=uv[2][1];Pc=uv[2][2];r=#Ip;b=#Pc;
    check(r==3*d0+1-g && b==g+2,"Schur block dimensions");
    Ainv=ZpXQMinv(ABCD[1],T,q2,p,2*eini);
    C=EMul(ABCD[3],Ainv,T,q2);AB=EMul(Ainv,ABCD[2],T,q2);
    rho=Ered(ABCD[4]-EMul(C,ABCD[2],T,q2),T,q2)/q;
    check(denominator(rho)==1,"integral lifting residual");
    cols=vector(2*d0+1,j,if(j<=2*d0,
      PicLift_worker_streamed(U0[,(j-1)%d0+1],((j-1)\d0)*nV,uv,AB,C,T,q,V),EFlatten(rho)));
    K=Mat(cols);m=matsize(K)[1];n=#K;
    check([m,n]==[(nZ-r)*b,2*d0+1],"full equation dimensions");
    L=LiftMatker_batched(K,T,q,p,eini);
    check(#L==d0+1,"known smooth divisor dimension");

    \\ Right annihilator N has rows -A^-1 B on P and identity on Pc.
    N=matrix(2*nV,b,i,j,Pol(0,variable(T)));
    for(i=1,r,for(j=1,b,N[P[i],j]=-AB[i,j]));
    for(j=1,b,N[Pc[j],j]=Pol(1,variable(T)));
    S=EMul(V,U0,T,q);
    H=vector(2,i,EMul(V,Erows(N,vector(nV,j,(i-1)*nV+j)),T,q));
    R=matrix(0,n);maxblock=0;equal_entries=0;
    for(k=1,b,
      block=RowBlock(k,H,S,C,Ip,Ic,rho,T,q);
      \\ Upstream mat2col visits matrix rows first, then columns.
      check(valuation(Ered(block-Erows(K,vector(#Ic,j,(j-1)*b+k)),T,q),p)>=eini,"row formula versus original columns");
      equal_entries+=#Ic*n;maxblock=max(maxblock,sizebyte(block));
      RR=EImage(matconcat([R;block])~,T,p);
      R=if(#RR,RR~,matrix(0,n));
    );
    LS=matkerpadic(R,T,q,p,eini);
    check(#LS==#L && #EIndex(matconcat([L,LS]),T,p)[2]==#L,"same free kernel");
    for(k=1,b,
      block=RowBlock(k,H,S,C,Ip,Ic,rho,T,q);
      check(valuation(EMul(block,LS,T,q),p)>=eini,"every streamed equation at full precision");
    );
    zero=0;full_degree=0;degree_sum=0;entry_bytes=0;witness=0;
    for(i=1,m,for(j=1,n,
      z=K[i,j]; entry_bytes+=sizebyte(z);
      z=liftall(Mod(z,p));
      if(z==0,zero++,
        dz=poldegree(z,variable(T));degree_sum+=dz;full_degree+=(dz==a-1);
        if(!witness,
          v=subst(z,variable(T),alpha)*alpha^0;
          if(a==2 && v^p!=v,witness=1);
          if(a==51 && v^(p^3)!=v && v^(p^17)!=v,witness=1);
        );
      );
    ));
    check(witness,"equation entries genuinely use the full residue field");
    check(equal_entries==m*n,"every matrix entry compared");
    listput(results,Str("{\"initial_precision\":",eini,",\"derivative_precision\":",eini,
      ",\"rows\":",m,",\"columns\":",n,",\"rank\":",n-#L,
      ",\"kernel_dimension\":",#L,",\"matrix_size_bytes\":",sizebyte(K),
      ",\"entry_payload_bytes\":",entry_bytes,",\"zero_entries_mod_p\":",zero,
      ",\"full_degree_entries_mod_p\":",full_degree,",\"degree_sum_mod_p\":",degree_sum,
      ",\"full_field_witness\":true,\"compared_entries\":",equal_entries,
      ",\"maximum_row_block_bytes\":",maxblock,",\"selected_rows\":",matsize(R)[1],
      ",\"selected_row_bytes\":",sizebyte(R),",\"row_formula_cache_bytes\":",sizebyte([S,H,C,rho]),
      ",\"timing_ms\":",getwalltime()-t0,"}"));
  );
  print("DATA|{\"genus\":",g,",\"p\":",p,",\"a\":",a,",\"precision_exponent\":",e,
    ",\"evaluation_points\":",nZ,",\"frobenius_cycle_lengths\":",Vec(cycles),
    ",\"systems\":[",results[1],",",results[2],"]}");
  print("PASS|106_lifttors_row_system");
}
quit;
