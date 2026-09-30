/* Reuse the exact local reduction, then check its alignment with every
   numerical side action before exporting data for the Belyi solver. */
default(realprecision,57);
read("../../pari/66_local_s3_cover.gp");
cg_pair(z)=[real(z),imag(z)];
cg_normalize(ab)=ab/sqrt(real(ab[1]*conj(ab[1])-ab[2]*conj(ab[2])));
cg_recenter(ab,c)={
  my(a=ab[1],b=ab[2],d=1-norm(c));
  cg_normalize([(a+b*conj(c)-c*(conj(b)+conj(a)*conj(c)))/d,
                (a*c+b-c*(conj(b)*c+conj(a)))/d]);
};
{
  my(ba=X[9],acts=afuchactions(X),err=0);
  if(#acts!=#sideelts,error("action/element counts differ"));
  for(i=1,#acts,
    my(a=cg_normalize(acts[i]),b=cg_normalize(sum(j=1,#sideelts[i],sideelts[i][j]*ba[j])));
    err=max(err,min(norml2(a-b),norml2(a+b)));
  );
  if(err>1e-80,error("side actions do not align with exact quaternion elements"));
  my(e=cg_normalize(sum(j=1,#elliptic[#elliptic],elliptic[#elliptic][j]*ba[j])));
  my(roots=polroots(conj(e[2])*x^2+(conj(e[1])-e[1])*x-e[2]));
  my(cm=if(abs(roots[1])<1,roots[1],roots[2]),er=cg_recenter(e,cm));
  my(turn=round(arg(er[1]/conj(er[1]))*32/(2*Pi)));
  if(turn%2==0 || abs(er[2])>1e-40,error("elliptic generator is not a primitive order-32 rotation"));
  my(file=Str(fdom_output,"/cover_geometry.json"));
  write(file,"{\"schema\":1,\"side_images\":",sideimages,",");
  write(file,"\"elliptic_image\":",ep[#ep],",\"elliptic_rotation_turn\":",turn,",");
  write(file,"\"alignment_squared_error\":",err,",");
  write(file,"\"cm_actions\":",vector(#acts,i,my(a=cg_recenter(cg_normalize(acts[i]),cm));[cg_pair(a[1]),cg_pair(a[2])]),"}");
  print("R80C|aligned ",#acts," exact side images with numerical actions; squared error=",err);
  print("PASS|80_cover_geometry");
}
