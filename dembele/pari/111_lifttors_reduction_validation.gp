\\ D66: precision reduction must commute with projective evaluation.
default(nbthreads,1);
setrand(20260917);
read("../../pari/.build/lifttors_reduction/install.gp");
check(ok,message)=if(!ok,error(message));
Ered(A,T,q)=liftall(Mod(Mod(A,T),q));
ProjectiveEqual(A,B,T,p,q)=
{
  my(pivot=0);
  check(type(A)=="t_COL" && type(B)=="t_COL" && #A==#B,"projective coordinate shape");
  check(valuation(A,p)==0 && valuation(B,p)==0,"primitive projective vectors");
  for(i=1,#B,if(valuation(B[i],p)==0,pivot=i;break));
  check(pivot>0,"unit coordinate");
  Ered(A*B[pivot]-B*A[pivot],T,q)==vector(#A,i,0)~;
};
{
  S=read("../../data/computed/lifttors_q8_control.bin");
  if(#S!=6 || #S[1]!=16,S=S[#S]);
  J=S[1];BL=S[3];p=Jgetp(J);T=JgetT(J);precs=[1,2,8,32,64];
  full=apply(W->PicEval(J,W),BL);tables=0;points=0;coordinates=0;compositions=0;rejections=0;
  for(k=1,#precs,
    e=precs[k];q=p^e;Je=PicRed(J,e);old=PicRed_original(J,e);
    for(i=1,16,if(i!=13,check(Je[i]==old[i],"unaffected Jacobian component")));
    check(Je[13][3..4]==old[13][3..4],"unaffected evaluation coordinate map");
    for(i=1,2,
      check(Je[13][i]==liftall(Mod(J[13][i],q)),"auxiliary reduction equals independent GP arithmetic");
      check(type(Je[13][i])=="t_VEC" && #Je[13][i]==#J[13][i],"embedding vector shape");
      for(j=1,#Je[13][i],
        check(type(Je[13][i][j])=="t_MAT" && matsize(Je[13][i][j])==matsize(J[13][i][j]),"embedding matrix shape");
        tables++;
      );
    );
    check(PicRed(Je,e)==Je,"idempotence");
    for(h=1,k,check(PicRed(Je,precs[h])==PicRed(J,precs[h]),"composition of reductions");compositions++);
    for(i=1,#BL,
      A=PicEval(Je,liftall(Mod(BL[i],q)));B=Ered(full[i],T,q);
      check(matsize(A)==matsize(B),"evaluation embedding pairs");
      for(c=1,#A,for(r=1,matsize(A)[1],
        check(ProjectiveEqual(A[r,c],B[r,c],T,p,q),"evaluation commutes with reduction");
        coordinates++;
      ));
      points++;
    );
  );
  for(i=1,2,
    bad=J;
    if(i==1,bad[13][1]=old[13][1],bad[13][1][1]=[1,2]);
    rejected=0;
    iferr(PicRed(bad,1),err,
      check(Str(err)=="error(\"PicRed: expected an embedding vector of matrices.\")","specific malformed-table error");
      rejected=1;
    );
    check(rejected,"malformed auxiliary table rejected");rejections++;
  );
  print("DATA|{\"genus\":2,\"p\":",p,",\"a\":2,\"precisions\":",precs,
    ",\"embedding_counts\":",vector(2,i,#J[13][i]),",\"embedding_matrices_checked\":",tables,
    ",\"point_evaluations_checked\":",points,",\"projective_vectors_checked\":",coordinates,
    ",\"composition_checks\":",compositions,",\"malformed_table_rejections\":",rejections,"}");
  print("PASS|111_lifttors_reduction_validation");
}
quit;
