/* Export disk actions at the generic center and the order-32 CM center. */
if(type(fdom_output)!="t_STR",fdom_output="../../data/computed");
cpair(z)=[real(z),imag(z)];
normalized(ab)={my(d=real(ab[1]*conj(ab[1])-ab[2]*conj(ab[2])));if(d<=0,error("nonpositive determinant"));ab/sqrt(d)};
recenter(ab,c)={
  my(a=ab[1],b=ab[2],d=1-norm(c));
  normalized([(a+b*conj(c)-c*(conj(b)+conj(a)*conj(c)))/d,
              (a*c+b-c*(conj(b)*c+conj(a)))/d]);
};
{
  default(realprecision,57);
  X=read("../../data/computed/normalizer_domain.bin");
  E=afuchelliptic(X); basisactions=X[9];
  emats=vector(#E,i,normalized(sum(j=1,#E[i],E[i][j]*basisactions[j])));
  e=emats[#emats];
  roots=polroots(conj(e[2])*x^2+(conj(e[1])-e[1])*x-e[2]);
  cm=if(abs(roots[1])<1,roots[1],roots[2]);
  if(abs(cm)>=1,error("no elliptic fixed point in disk"));
  check=recenter(e,cm);
  if(abs(check[2])>1e-40,error("CM conjugation did not diagonalize elliptic element"));
  if(abs((check[1]/conj(check[1]))^32-1)>1e-40,error("wrong elliptic rotation"));
  actions=vector(#afuchactions(X),i,normalized(afuchactions(X)[i]));
  cm_actions=vector(#actions,i,recenter(actions[i],cm));
  file=Str(fdom_output,"/expansion_geometry.json");
  write(file,"{\"cm\":",cpair(cm),",");
  write(file,"\"elliptic_orders\":",Vec(afuchsignature(X)[2]),",");
  write(file,"\"elliptic_actions\":",vector(#emats,i,[cpair(emats[i][1]),cpair(emats[i][2])]),",");
  write(file,"\"actions\":",vector(#actions,i,[cpair(actions[i][1]),cpair(actions[i][2])]),",");
  write(file,"\"cm_actions\":",vector(#actions,i,[cpair(cm_actions[i][1]),cpair(cm_actions[i][2])]),",");
  write(file,"\"vertices\":",vector(#afuchvertices(X),i,cpair(klein_to_disc(afuchvertices(X)[i]))),"}");
  print("R67|CM point in original disk=",cm);
  print("R67|conjugated elliptic off-diagonal=",abs(check[2]));
  print("R67|side actions exported=",#actions,"; max CM-centered |A|=",vecmax(vector(#actions,i,abs(cm_actions[i][1]))));
  print("PASS|67_expansion_geometry");
}
