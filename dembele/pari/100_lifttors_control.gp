\\ Run from vendor/LiftTors after build_lifttors.py. One block: errors
\\ prevent the PASS marker. This is the known Q8 control, not target Y.
default(nbthreads,1);
setrand(20260916);
read("../../pari/.build/lifttors/install.gp");
read("GalRep.gp");
read("PtIsOnCurve.gp");
check(ok,message)=if(!ok,error(message));
{
  p=7; a=2; e=64; ell=2;
  t0=getwalltime();
  f=15*x^6+79*x^5+160*x^4+160*x^3+80*x^2+16*x;
  check(f==x^6*subst(16*x^5-x,x,1+1/x),"birational change");
  w=Mod(z,z^4-1080*z^2+230400);
  P1=[1,(w^2+480)/(2*w)]; P2=[2,16*(w^2-480)/(2*w)];
  check(PtIsOnHyperCurve(f,P1) && PtIsOnHyperCurve(f,P2),"auxiliary points");
  C=Hyper2RR(f,P1,P2);
  Lp=hyperellcharpoly(Mod(f,p));
  check(Lp==hyperellcharpoly(Mod(16*x^5-x,p)),"Euler factor after coordinate change");
  check(polresultant(Lp,x^a-1)==4096,"independent Magma cardinality");
  J=PicInit(C[1],C[2],C[4],C[5],C[6..9],y,p,a,e);
  nZ=#J[14];
  check(Jgetg(J)==2 && J[3]==6 && nZ>5*J[3],"Makdisi dimensions");
  dims=vector(3,i,matsize(J[10][i])[2]);
  check(dims==[5,11,17],"section dimensions");
  init_ms=getwalltime()-t0;
  \\ Prove the divisor/lifting/evaluation backend only needs arithmetic
  \\ evaluation data. Automatic precision increase would need a frontend.
  J[1]=0; J[4]=[]; J[14]=[];
  J1=PicRed(J,1);
  t0=getwalltime();
  [B,M,MA]=TorsBasis(J1,ell,Lp,0,C[3]);
  check(#B==4 && M^2==1 && matrank(M-1)==1,"Frobenius versus Magma");
  basis_ms=getwalltime()-t0;
  t0=getwalltime();
  BL=apply(W->PicLiftTors(J,W,1,ell),B);
  lift_ms=getwalltime()-t0;
  for(i=1,4,
    check(PicMember_val(J,BL[i])==e,"lift is a Jacobian point");
    check(PicIsTorsion_val(J,BL[i],ell)==e,"lift killed by 2");
    check(PicEq_val(J1,liftall(Mod(BL[i],p)),B[i])==1,"lift reduces to input");
    check(PicEq_val(J,PicFrob(J,BL[i]),PicLC(J,lift(M[,i]),BL))==e,"lifted Frobenius");
  );
  \\ Exhaustive independence on reduction, not only pairing rank.
  pts=vector(16,k,PicLC(J1,vector(4,j,bittest(k-1,j-1))~,B));
  for(i=1,16,for(j=i+1,16,check(PicEq_val(J1,pts[i],pts[j])==0,"distinct points")));
  fixed=sum(i=1,16,PicEq_val(J1,pts[i],PicFrob(J1,pts[i])));
  check(fixed==8,"eight Frobenius-fixed points including zero");
  t0=getwalltime();
  [WB,cWB]=TorsSpaceFrobGen(J,ell,BL,M);
  Z=TorsSpaceFrobEval(J,WB,cWB,ell,M,MA);
  check(#Z[1]==11,"eleven nonzero Frobenius orbits");
  eval_ms=getwalltime()-t0;
  t0=getwalltime();
  AF=TorsSpaceGetPols(Z,ell,M,JgetFrobMat(J),JgetT(J),Jgetpe(J),p,e);
  check(#AF>0,"at least one separating recognized polynomial");
  F=AF[1][3]; roots=AF[1][1];
  check(poldegree(F)==15 && poldegree(gcd(F,deriv(F)))==0,"degree and separability");
  check(#Set(roots)==15,"all nonzero torsion separated");
  check(vecmin(apply(r->valuation(lift(subst(F,x,r)),p),roots))>=e,"recognized polynomial matches all p-adic values");
  factors=factor(F); linear=0; quadratic=0;
  for(i=1,matsize(factors)[1],
    check(factors[i,2]==1,"squarefree factors");
    d=poldegree(factors[i,1]);
    if(d==1,linear++,
      check(d==2,"only linear and quadratic factors"); quadratic++;
      check(issquare(-poldisc(factors[i,1])),"each quadratic cuts out Q(i)");
    );
  );
  check(linear==7 && quadratic==4,"independent torsion Galois orbit sizes");
  poly_ms=getwalltime()-t0;
  print("DATA|{\"genus\":2,\"d0\":6,\"p\":7,\"a\":2,\"precision_exponent\":",e,
    ",\"evaluation_points\":",nZ,",\"section_dimensions\":",dims,
    ",\"torsion_count\":16,\"frobenius_fixed_count\":",fixed,
    ",\"frobenius_rows\":",vector(4,i,Vec(lift(M[i,]))),
    ",\"polynomial_coefficients_ascending\":",vector(16,i,Str(polcoef(F,i-1))),
    ",\"factor_degrees\":",vector(matsize(factors)[1],i,poldegree(factors[i,1])),
    ",\"timing_ms\":{\"init\":",init_ms,",\"basis\":",basis_ms,
    ",\"lift_four_points\":",lift_ms,",\"span_and_evaluate\":",eval_ms,
    ",\"polynomial_and_checks\":",poly_ms,"}}");
  writebin("../../data/computed/lifttors_q8_control.bin",[J,B,BL,M,Z,AF[1]]);
  print("PASS|100_lifttors_control");
}
quit;
