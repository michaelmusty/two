\\ D66: object-tree storage of a correctly reduced degree-51 Jacobian.
\\ No torsion lift or genus-64 object is constructed here.
default(nbthreads,1);
setrand(20260916);
read("../../pari/.build/lifttors_reduction/install.gp");
check(ok,message)=if(!ok,error(message));
RRinf(n,g)=concat(vector(n\2+1,j,x^(j-1)),if(n<2*g+1,[],vector((n-2*g-1)\2+1,j,y*x^(j-1))));
MatrixStats(M,q)=
{
  my(m=matsize(M)[1],n=#M,zeros=0,units=0,entrybytes=0,nontrivialbytes=0,v,b);
  for(j=1,n,for(i=1,m,
    v=M[i,j];b=sizebyte(v);entrybytes+=b;
    if(v==0,zeros++,if(v==1 || v==q-1,units++,nontrivialbytes+=b));
  ));
  Str("{\"rows\":",m,",\"columns\":",n,",\"object_bytes\":",sizebyte(M),
    ",\"zero_entries\":",zeros,",\"unit_constant_entries\":",units,
    ",\"entry_bytes\":",entrybytes,",\"nontrivial_entry_bytes\":",nontrivialbytes,"}");
};
{
  g=16;a=51;p=97;e=4;d0=2*g+1;
  J=PicInit(y^2-(x^(2*g+1)-x),[],g,d0,
    [RRinf(d0,g),RRinf(2*d0,g),RRinf(3*g+1,g),RRinf(3*g+1,g)],y,p,a,e);
  T=JgetT(J);nZ=#J[14];alpha=ffgen(Mod(T,p),'u);witness=0;
  check(poldegree(T)==a && polisirreducible(Mod(T,p)),"actual residue degree");
  visited=vector(nZ);cycles=List();
  for(i=1,nZ,if(!visited[i],j=i;n=0;while(!visited[j],visited[j]=1;n++;j=J[15][j]);listput(cycles,n)));
  check(Vec(cycles)==[51,51,51,51],"four full Frobenius cycles");
  for(j=1,#J[10][2],for(i=1,nZ,
    v=subst(J[10][2][i,j],variable(T),alpha);
    if(v^(p^3)!=v && v^(p^17)!=v,witness=1;break);
  );if(witness,break));
  check(witness,"section entry outside both maximal proper subfields");
  J[1]=0;J[4]=[];J[14]=[];
  check(sizebyte(J)==120428336,"same seeded Jacobian as the degree-51 scale control");
  records=List();
  for(k=1,3,
    e=[1,2,4][k];Je=PicRed(J,e);
    check(Je[13][1]==liftall(Mod(J[13][1],p^e)) && Je[13][2]==liftall(Mod(J[13][2],p^e)),"correct auxiliary tables");
    matrices=List();
    for(i=1,3,listput(matrices,Str("\"V",i,"\":",MatrixStats(Je[10][i],p^e))));
    for(i=1,3,listput(matrices,Str("\"KV",i,"\":",MatrixStats(Je[11][i],p^e))));
    listput(matrices,Str("\"W0\":",MatrixStats(Je[12],p^e)));
    for(i=1,2,check(#Je[13][i]==1,"rational auxiliary divisor");listput(matrices,Str("\"U",i,"\":",MatrixStats(Je[13][i][1],p^e))));
    listput(matrices,Str("\"evaluation_inverse\":",MatrixStats(Je[13][4],p^e)));
    listput(records,Str("{\"precision_exponent\":",e,",\"jacobian_size_bytes\":",sizebyte(Je),
      ",\"component_bytes\":",vector(16,i,sizebyte(Je[i])),",\"matrices\":{",strjoin(Vec(matrices),","),"}}"));
  );
  print("DATA|{\"genus\":",g,",\"p\":",p,",\"a\":",a,",\"evaluation_points\":",nZ,
    ",\"frobenius_cycle_lengths\":",Vec(cycles),",\"full_field_entry_witness\":true,\"records\":[",strjoin(Vec(records),","),"]}");
  print("PASS|109_lifttors_storage");
}
quit;
