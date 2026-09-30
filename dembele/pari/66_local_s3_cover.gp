/* Exact local monodromy of the saved genus-16 normalizer presentation.
   Run after fdom.gp, from vendor/rickards-fdom. */
if(type(fdom_output)!="t_STR",fdom_output="../../data/computed");
{
  X=read("../../data/computed/normalizer_domain.bin");
  A=afuchalg(X); F=algcenter(A);
  p=idealprimedec(F,2)[1];
  A2=algtableinit(algmultable(A),2);
  rad=algradical(A2);
  quot=algquotient(A2,rad,1); Q=quot[1]; proj=quot[2];
  print("R66|O/2 dimension=",algdim(A2),"; radical dimension=",matsize(rad)[2],"; residue dimension=",algdim(Q));
  if(algdim(Q)!=2,error("residue algebra must have dimension 2 over F2"));
  nonzero=[[1,0]~,[0,1]~,[1,1]~];
  for(i=1,3,if(algpow(Q,nonzero[i],3)!=algpow(Q,nonzero[i],0),error("residue is not F4")));
  uniformizer=alg1ijktobasis(A,[0,1,0,0]~);
  if(idealval(F,algnorm(A,uniformizer),p)!=1,error("i is not a division uniformizer"));
  P=afuchpresentation(X); gens=P[1]; rels=P[2];
  print("R66|presentation generators=",#gens,"; relations=",#rels);
}

localimage(g)={
  my(v=idealval(F,algnorm(A,g),p), u, r, result);
  u=algmul(A,g,algpow(A,uniformizer,-v));
  r=lift(Mod(proj,2)*Mod(u,2));
  if(r==[0,0]~,error("normalized residue is zero"));
  result=vector(3,k,0);
  for(k=1,3,
    my(t=algmul(Q,r,algpow(Q,nonzero[k],2^(v%2))));
    for(j=1,3,if(t==nonzero[j],result[k]=j));
  );
  if(vecsort(result)!=[1,2,3],error("invalid residue permutation"));
  result;
};
pmul(a,b)=vector(3,i,a[b[i]]);
pinv(a)={my(b=vector(3));for(i=1,3,b[a[i]]=i);b};

{
  images=vector(#gens,i,localimage(gens[i]));
  for(i=1,#rels,
    my(r=rels[i], s=[1,2,3]);
    for(j=1,#r,s=pmul(s,if(r[j]>0,images[r[j]],pinv(images[-r[j]]))));
    if(s!=[1,2,3],error("a presentation relation fails in S3"));
  );
  /* Multiplicativity checks use exact quaternion products, independently
     of the presentation relations. */
  for(i=1,#gens,for(j=1,min(#gens,5),
    if(localimage(algmul(A,gens[i],gens[j]))!=pmul(images[i],images[j]),error("local map is not multiplicative"))));
  G=Set(concat([[1,2,3]],images));
  until(#G==6 || #G==oldsize,
    oldsize=#G;
    for(i=1,#G,for(j=1,#images,G=setunion(G,Set([pmul(G[i],images[j])]))));
  );
  if(#G!=6,error("local image is not all S3"));
  elliptic=afuchelliptic(X);
  ep=vector(#elliptic,i,localimage(elliptic[i]));
  print("R66|elliptic images=",ep);
  orders=Vec(afuchsignature(X)[2]);
  residualorders=vector(#ep,i,if(ep[i]==[1,2,3],1,if(pmul(ep[i],ep[i])==[1,2,3],2,3)));
  if(residualorders!=concat(concat(vector(17,i,2),vector(9,i,3)),[2]),error("wrong elliptic monodromy"));
  yorders=concat(vector(17,i,2),[16,32]);
  zorders=[16,16,16];
  orbC=1455/32;
  gY=1+(3*orbC-sum(i=1,#yorders,1-1/yorders[i]))/2;
  gZ=1+(6*orbC-sum(i=1,#zorders,1-1/zorders[i]))/2;
  if(gY!=64 || gZ!=136,error("cover genera disagree"));
  print("R66|verified local elliptic orders=",residualorders);
  print("R66|Y signature=(",gY,"; ",yorders,"); Z signature=(",gZ,"; ",zorders,")");
  /* An independent rational homology check from the lifted presentation:
     C_1 has one oriented edge for each generator and each of 3 sheets.
     Use the right action s*g = image(g)^(-1)(s). */
  ng=#gens; d1=matrix(3*ng,3); d2=matrix(3*#rels,3*ng);
  for(s=1,3,for(j=1,ng,
    my(e=(s-1)*ng+j, t=pinv(images[j])[s]);
    d1[e,s]-=1; d1[e,t]+=1;
  ));
  for(s=1,3,for(i=1,#rels,
    my(t=s,r=rels[i],row=(s-1)*#rels+i);
    for(k=1,#r,
      my(j=abs(r[k]),next);
      if(r[k]>0,
        d2[row,(t-1)*ng+j]+=1; t=pinv(images[j])[t],
        next=images[j][t]; d2[row,(next-1)*ng+j]-=1; t=next
      );
    );
    if(t!=s,error("lifted relation does not close"));
  ));
  if(d2*d1!=matrix(3*#rels,3),error("cellular boundary square nonzero"));
  betti=3*ng-matrank(d1)-matrank(d2);
  if(betti!=128,error("wrong first Betti number for Y"));
  print("R66|lifted rational homology: rank(d1)=",matrank(d1),"; rank(d2)=",matrank(d2),"; b1=",betti);
  sideelts=afuchelts(X);
  sideimages=vector(#sideelts,i,localimage(sideelts[i]));
  repwords=vector(3,i,[]); reps=vector(3); seen=[1,0,0];
  reps[1]=algpow(A,gens[1],0);
  for(s=1,3,if(seen[s],for(j=1,#sideelts,
    my(t=pinv(sideimages[j])[s]);
    if(!seen[t],seen[t]=1;repwords[t]=concat(repwords[s],[j]);reps[t]=algmul(A,reps[s],sideelts[j]));
  )));
  if(seen!=[1,1,1],error("side generators do not reach all cover sheets"));
  for(s=1,3,for(j=1,#sideelts,
    my(t=pinv(sideimages[j])[s],h=algmul(A,algmul(A,reps[s],sideelts[j]),alginv(A,reps[t])));
    if(localimage(h)[1]!=1,error("Schreier generator not in reflection subgroup"));
  ));
  print("R66|coset representatives in side generators=",repwords,"; all Schreier generators fix sheet 1");
  radii=vecsort(vector(#afuchvertices(X),j,abs(klein_to_disc(afuchvertices(X)[j]))));
  print("R66|disk vertex radii min/median/max=",[radii[1],radii[#radii\2],radii[#radii]]);
  print("R66|geometric damping only: max_radius^N < 10^-30 needs N=",ceil(-30*log(10)/log(radii[#radii])),"; not a truncation-error certificate");
  write(Str(fdom_output,"/normalizer_s3_images.gp"),[images,ep]);
  write(Str(fdom_output,"/genus64_cosets.gp"),[sideimages,repwords,reps]);
  print("R66|all presentation relations and product checks pass; image order=",#G);
  print("PASS|66_local_s3_cover");
}
