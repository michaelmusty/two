"""D116: exact saturation of the existing integer harmonic cocycle lattice.

This is a lattice of tree cocycles, not an asserted stable dualizing lattice.
All Smith operations are saved as a replayable unimodular witness.
"""
from fractions import Fraction as Q
import hashlib
import json
from math import prod
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'

def source(path):
    p=Path(path).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def smith(B):
    a=[row[:] for row in B];m,n=len(a),len(a[0]);U=[[int(i==j) for j in range(m)] for i in range(m)];operations=[]
    def row_swap(i,j):
        a[i],a[j]=a[j],a[i];U[i],U[j]=U[j],U[i];operations.append(['rs',i,j])
    def col_swap(i,j):
        for row in a:row[i],row[j]=row[j],row[i]
        operations.append(['cs',i,j])
    def row_add(i,j,q):
        a[i]=[x+q*y for x,y in zip(a[i],a[j])];U[i]=[x+q*y for x,y in zip(U[i],U[j])];operations.append(['ra',i,j,q])
    def col_add(i,j,q):
        for row in a:row[i]+=q*row[j]
        operations.append(['ca',i,j,q])
    for k in range(m):
        _,i,j=min((abs(a[i][j]),i,j) for i in range(k,m) for j in range(k,n) if a[i][j])
        if i!=k:row_swap(i,k)
        if j!=k:col_swap(j,k)
        while True:
            changed=False
            for i in range(k+1,m):
                if a[i][k]:
                    row_add(i,k,-(a[i][k]//a[k][k]))
                    if a[i][k]:row_swap(i,k)
                    changed=True;break
            if changed:continue
            for j in range(k+1,n):
                if a[k][j]:
                    col_add(j,k,-(a[k][j]//a[k][k]))
                    if a[k][j]:col_swap(j,k)
                    changed=True;break
            if changed:continue
            bad=next(((i,j) for i in range(k+1,m) for j in range(k+1,n) if a[i][j]%a[k][k]),None)
            if bad is None:break
            row_add(k,bad[0],1)
        if a[k][k]<0:
            a[k]=[-x for x in a[k]];U[k]=[-x for x in U[k]];operations.append(['rn',k])
    diagonal=[a[i][i] for i in range(m)]
    assert all(a[i][j]==(diagonal[i] if i==j else 0) for i in range(m) for j in range(n))
    assert all(y%x==0 for x,y in zip(diagonal,diagonal[1:]))
    saturated=[]
    for i in range(m):
        row=[sum(U[i][k]*B[k][j] for k in range(m)) for j in range(n)]
        assert all(x%diagonal[i]==0 for x in row)
        saturated.append([x//diagonal[i] for x in row])
    return diagonal,U,saturated,operations

def build():
    path=DATA/'dyadic_harmonic_certificate_d111.json';p=json.loads(path.read_text());B=p['harmonic_basis']
    diagonal,U,C,operations=smith(B)
    relations=p['harmonic_relations']
    assert all(sum(a*b for a,b in zip(row,c))==0 for row in relations for c in C)
    # A primitive vector basis need not be jointly saturated.
    control=[[1,1,0],[1,-1,0]];cd,_,_,_=smith(control);assert cd==[1,2]
    print('HARMONIC_SMITH|'+json.dumps(diagonal)+'|index='+str(prod(diagonal)),flush=True)
    return {'status':'pass','milestone':'D116','shape':[len(B),len(B[0])],
      'Smith_invariant_factors':diagonal,'index_in_integer_kernel':prod(diagonal),
      'row_unimodular_transform':U,'saturated_integer_harmonic_basis':C,
      'Smith_unimodular_operations':operations,'exact_relations_annihilate_saturated_basis':True,
      'primitive_vectors_do_not_imply_saturation_control':cd,
      'stable_dualizing_lattice_identified':False,'residue_frame_index_computed':False,
      'actual_moments_recomputed':False,'candidate_identification_proved':False,
      'sources':[source(x) for x in [Path(__file__),path,
          ROOT/'dembele/certificates/dyadic-harmonic-d111.md',
          ROOT/'dembele/certificates/cm-residue-lattice-d102.md']]}

if __name__=='__main__':
    result=build();out=DATA/'dyadic_harmonic_saturation_d116.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n');print('PASS|436_DYADIC_HARMONIC_SATURATION',flush=True)
