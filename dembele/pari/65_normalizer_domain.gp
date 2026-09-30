/* Run from vendor/rickards-fdom after loading fdom.gp; see pari/README.md.
   Dembélé, arXiv:1906.06772, section 5.1: D=(y-y^2,-1)/F.
   type=3 is the positive normalizer, whose curve is C of genus 16.
   All checks are in one block so an error prevents the PASS marker. */
if(type(fdom_output)!="t_STR",fdom_output="../../data/computed");
{
  default(realprecision,57);
  setrand(20260915);
  gettime();
  F=nfinit(y^8-8*y^6+20*y^4-16*y^2+2);
  print("R65|field discriminant=",F.disc);
  A=alginit(F,[y-y^2,-1]);
  print("R65|algebra and maximal order initialized; cpu_ms=",gettime());
  print("R65|finite Hasse invariants=",alghassef(A));
  print("R65|infinite Hasse invariants=",alghassei(A));
  X=afuchinit(A,,3,0);
  print("R65|normalizer initialized; cpu_ms=",gettime());
  print("R65|normalizer norm generators=",afuchnormalizernorms(X));
  X=afuchmakefdom(X);
  print("R65|fundamental domain built; cpu_ms=",gettime());
  S=afuchsignature(X);
  print("R65|signature=",S);
  if(S[1]!=16 || S[3]!=0,error("wrong genus or cusps"));
  if(Vec(S[2])!=concat(concat(vector(17,i,2),vector(9,i,3)),[32]),error("wrong elliptic orders"));
  if(afuchcheck(X)!=0,error("domain/presentation validation failed"));
  writebin(Str(fdom_output,"/normalizer_domain.bin"),X);
  write(Str(fdom_output,"/normalizer_domain_presentation.gp"),afuchpresentation(X));
  print("R65|sides=",#afuchsides(X),"; area/(2Pi)=",afucharea(X)/(2*Pi));
  print("PASS|65_normalizer_domain");
}
