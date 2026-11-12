"""D138 independent arithmetic review of the P=1600 frame and quadrics.

No production arithmetic module is imported. Multiplication uses Horner
steps in the integer polynomial quotient. Integral balls carry absolute
errors without normalizing to a unit or dividing during multiplication.
Run each phase through run_dyadic_capped.py with a fresh receipt stem.
"""
import argparse
from fractions import Fraction as Q
from functools import lru_cache
import hashlib
import json
import time
import resource
import sys
from math import comb, lcm
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]; DATA=ROOT/'dembele/data/computed'
FP=(2,0,-16,0,20,0,-8,0,1)
USED=set()


def read(stem):
    path=DATA/(stem+'.json'); USED.add(path)
    return json.loads(path.read_text())


def source(path):
    path=Path(path).resolve(); h=hashlib.sha256()
    with path.open('rb') as f:
        while block:=f.read(1<<20):h.update(block)
    return {'path':str(path),'sha256':h.hexdigest()}


def cm_polynomial():
    result=[0]*17; power=[1]
    for coefficient in FP:
        for i,x in enumerate(power):result[i]+=coefficient*x
        new=[0]*(len(power)+2)
        for i,x in enumerate(power):new[i]-=2*x;new[i+2]-=x
        power=new
    return tuple(result)


MP=cm_polynomial()


class Quotient:
    def __init__(self,poly,precision):
        self.poly=tuple(poly);self.n=len(poly)-1;self.precision=precision
        assert poly[-1]==1 and poly[0]==2 and precision%self.n==0
        self.mod=1<<(precision//self.n);self.mask=self.mod-1
        self.zero=(0,)*self.n;self.one=(1,)+(0,)*(self.n-1)
        self.beta=(0,1)+(0,)*(self.n-2)
    def norm(self,x):
        assert len(x)==self.n
        return tuple(int(c)&self.mask for c in x)
    def add(self,x,y):return tuple((a+b)&self.mask for a,b in zip(x,y))
    def scale(self,x,c):return tuple((a*c)&self.mask for a in x)
    def sub(self,x,y):return tuple((a-b)&self.mask for a,b in zip(x,y))
    def mul(self,x,y):
        if x==self.zero or y==self.zero:return self.zero
        if x==self.one:return y
        if y==self.one:return x
        out=[0]*self.n
        # Horner evaluation of x(beta)*y, reducing once per beta step.
        for c in reversed(x):
            carry=out[-1]
            out=[(c*y[0]-carry*self.poly[0])&self.mask]+[
                (out[i-1]+c*y[i]-carry*self.poly[i])&self.mask for i in range(1,self.n)]
        return tuple(out)
    def value(self,x):
        return min([self.precision]+[self.n*((c&-c).bit_length()-1)+i for i,c in enumerate(x) if c])
    def rational(self,row):
        out=[]
        for c in row:
            q=Q(c);assert q.denominator%2
            out.append(q.numerator*pow(q.denominator,-1,self.mod)&self.mask)
        return tuple(out)
    def evaluate(self,poly,x):
        out=self.zero
        for c in reversed(poly):out=self.add(self.mul(out,x),self.scale(self.one,c))
        return out
    @lru_cache(None)
    def power_beta(self,n):
        assert n>=0
        result=self.one;x=self.beta
        while n:
            if n&1:result=self.mul(result,x)
            x=self.mul(x,x);n//=2
        return result
    def divide_beta(self,x,n):
        for _ in range(n):
            assert x[0]%2==0
            c=x[0]//2
            x=tuple(((x[i+1] if i+1<self.n else 0)-c*self.poly[i+1])&self.mask for i in range(self.n))
        return x


def comparison_review():
    bank=read('dyadic_precision1600_bank_d138');frame=read('dyadic_residue_frame1600_d138')
    eta=read('dyadic_CM_frame_beta21168_d122');candidate=read('cm_frame_curve_candidate')
    quadrics=read('dyadic_integral_quadrics1600_d138');old=read('dyadic_precision400_d122')
    design=read('dyadic_precision_design_d120')['precision_design']
    budget=read('cm_arithmetic_height_budget_d118')['budgets']
    ring=Quotient(MP,8192)

    class Ball:
        def __init__(self,x=None,error=8192):
            self.x=ring.zero if x is None else ring.norm(x);self.error=min(error,ring.precision)
        def lower(self):return min(ring.value(self.x),self.error)
        def nonzero(self):return ring.value(self.x)<self.error
        def __add__(self,y):return Ball(ring.add(self.x,y.x),min(self.error,y.error))
        def __neg__(self):return Ball(ring.scale(self.x,-1),self.error)
        def __sub__(self,y):return self+(-y)
        def __mul__(self,y):
            return Ball(ring.mul(self.x,y.x),min(self.error+y.lower(),y.error+self.lower()))
        def scale(self,c):
            if not c:return Ball()
            return Ball(ring.scale(self.x,c),self.error+16*((abs(c)&-abs(c)).bit_length()-1))
        def divide_beta(self,n):
            assert self.lower()>=n
            return Ball(ring.divide_beta(self.x,n),self.error-n)

    def power(n):return Ball(ring.power_beta(n))
    def saved(row,shift=0,exact=False):
        v=row['beta_exponent']
        if v is None:return Ball(error=8192 if exact else row['error_beta']+shift)
        assert v+shift>=0
        return Ball(ring.mul(ring.norm(row['unit_beta']),ring.power_beta(v+shift)),
                    8192 if exact else row['error_beta']+shift)
    def dot(xs,ys):
        value=Ball()
        for x,y in zip(xs,ys):value=value+x*y
        return value
    def check_enclosure(value,record):
        expected=saved(record)
        assert not(value-expected).nonzero()
        assert value.error>=record['error_beta'],(value.error,record['error_beta'])
        assert value.lower()>=expected.lower()

    assembled=0
    for col,record in enumerate(bank['state_columns']):
        packet=read(Path(record['CM_metadata']['path']).stem)
        assert packet['working_precision_pi']==(6400 if col==0 else 1600) and packet['harmonic_basis_column']==col
        for ci in range(17):
            for n in range(4):
                assert [x%(1<<204) for x in packet['CM_values'][ci]['coarse_coefficients_beta'][n]]==bank['CM_values'][ci]['coarse_coefficients_beta'][n][col]
                assembled+=1
    assert assembled==1088
    raw=[[[Ball(cs,bank['coarse_error_beta'][n]) for cs in row['coarse_coefficients_beta'][n]]
           for n in range(4)] for row in bank['CM_values']]
    H=[[x.divide_beta(296 if i==0 else 33) for x in jet[0]] for i,jet in enumerate(raw)]
    assert design['nonanchor_evaluation_Smith_beta']==[0]*8+[35]*8
    assert design['nonanchor_inverse_entry_lower_beta']==-35
    overlap=[]
    for row,previous in zip(H[1:],old['CM_values'][1:]):
        for x,y in zip(row,previous['coarse_coefficients_beta'][0]):
            before=Ball(y,old['coarse_error_beta'][0]).divide_beta(33)
            overlap.append((x-before).lower());assert overlap[-1]>35
    # Neumann stability transfers the audited inverse norm -35 from D120.
    Qcenters=[saved(x,shift=35,exact=True) for x in frame['frame_relation']]
    assert all(x.lower()==0 for x in Qcenters)
    qres=[dot(Qcenters,[row[j] for row in H[1:]])-power(35)*H[0][j] for j in range(16)]
    assert all(not x.nonzero() for x in qres)
    qbound=min(x.lower() for x in qres)-70
    assert all(x['error_beta']<=qbound for x in frame['frame_relation'])
    Qballs=[saved(x,shift=35) for x in frame['frame_relation']]
    change_centers=[[saved(x,exact=True) for x in row] for row in frame['change_of_basis']]
    etaballs=[[Ball(x,min(4096,eta['rational_residue_frame_error_beta'])) for x in row] for row in eta['rational_residue_frame_values']]
    change_bounds=[]
    for j in range(16):
        column=[row[j] for row in change_centers]
        residual=[Qballs[i]*dot(H[i+1],column)-power(35)*etaballs[i+1][j] for i in range(16)]
        assert all(not x.nonzero() for x in residual)
        bound=min(x.lower() for x in residual)-35;change_bounds.append(bound)
        assert all(row[j]['error_beta']<=bound for row in frame['change_of_basis']), (j,bound)
    change=[[saved(x) for x in row] for row in frame['change_of_basis']]
    pairs=candidate['monomial_pairs'];counts=0;mismatches=[];minimums=[];gaussians=[]
    for ci,jet in enumerate(raw):
        actual=[[dot(row,col) for col in zip(*change)] for row in jet]
        for row,expected in zip(actual,frame['CM_values'][ci]['actual_residue_frame_coarse_jets']):
            for x,y in zip(row,expected):check_enclosure(x,y)
        for j in range(16):
            relation=actual[0][j]+power(296)*etaballs[0][j] if ci==0 else Qballs[ci-1]*actual[0][j]-power(68)*etaballs[ci][j]
            assert not relation.nonzero()
        x,v,w,t=actual;G=x[0]*v[1]-x[1]*v[0]
        gaussians.append({'valuation_beta':ring.value(G.x) if G.nonzero() else None,'error_beta':G.error})
        assert gaussians[-1]['valuation_beta']==frame['Gaussian_G12'][ci]['valuation_beta']
        assert G.error>=frame['Gaussian_G12'][ci]['error_beta']
        xsquares=[x[i]*x[j] for i,j in pairs];vsquares=[v[i]*v[j] for i,j in pairs]
        mins=[10**9]*4;m=296 if ci==0 else 33
        for qi,coeff in enumerate(candidate['quadrics']):
            gx=[Ball() for _ in range(16)];gv=[Ball() for _ in range(16)];Qx=Ball();Qv=Ball()
            for c,(i,j),xx,vv in zip(coeff,pairs,xsquares,vsquares):
                if not c:continue
                gx[i]=gx[i]+x[j].scale(c);gx[j]=gx[j]+x[i].scale(c)
                gv[i]=gv[i]+v[j].scale(c);gv[j]=gv[j]+v[i].scale(c)
                Qx=Qx+xx.scale(c);Qv=Qv+vv.scale(c)
            values=[Qx,dot(gx,v),dot(gx,w)+Qv,dot(gx,t)+dot(gv,w)]
            expected=quadrics['CM_values'][ci]['all_91_quadric_coefficients'][qi]
            for n,(value,row) in enumerate(zip(values,expected)):
                check_enclosure(value,row['coarse_coefficient'])
                assert value.nonzero()==row['coarse_known_nonzero']
                if value.nonzero():mismatches.append((ci,qi,n))
                lower=saved(row['coarse_coefficient']).lower()+2*3920-4200-(n+2)*m
                assert lower==row['conditional_intrinsic_jet_lower_beta']
                assert row['required_exact_vanishing_already_proved']==(n<=1)
                mins[n]=min(mins[n],lower);counts+=1
        assert mins==quadrics['CM_values'][ci]['minimum_lower_beta_by_order']
        minimums.append(mins)
        print(f'INDEPENDENT_QUADRICS|CM={ci}; scalars={counts}',flush=True)
    assert counts==6188 and bool(mismatches)==quadrics['candidate_mismatch_certified']
    x=Q(1,3);lo=2*sum(x**(2*k+1)/Q(2*k+1) for k in range(80))
    hi=lo+2*x**161/(161*(1-x*x));thresholds=[]
    for n,savedrow in enumerate(quadrics['comparison_with_sufficient_bounds'],1):
        lower,upper=map(Q,budget['thresholds'][n-1]['upper_bound_expression_interval'])
        N=min(row[n] for row in minimums[1:]);A=minimums[0][n]
        target=savedrow['sufficient_nonanchor_beta_with_new_anchor']
        assert (16*target+A)*lo>272*upper
        assert (16*(target-1)+A)*hi<272*lower
        assert savedrow['degree16_achieved_lower_beta']==N and savedrow['anchor_achieved_lower_beta']==A
        assert (16*N+A)*hi<272*lower and not savedrow['inequality_is_sufficient']
        thresholds.append(target)
    return {'all_bank_assembled_coarse_values_checked':assembled,'frame_relation_certified_error_beta':qbound,'change_column_error_bounds_beta':change_bounds,
        'inherited_inverse_norm_preserved_by_overlap_beta':min(overlap),'all_actual_jet_values_checked':17*4*16,
        'independent_quadric_coefficients_checked':counts,'positive_coefficients_checked':4641,
        'certified_mismatch_count':len(mismatches),'degree16_section_lower_beta':[min(x[n] for x in minimums[1:]) for n in (1,2,3)],
        'anchor_section_lower_beta':minimums[0][1:],'sufficient_nonanchor_beta':thresholds,
        'W_Gaussian':gaussians[0],'W_Gaussian_inverted':False,'positive_exact_vanishing_proved':False,
        'method':'integer quotient absolute-error balls, frame residual bounds, gradients and polar forms'}


if __name__=='__main__':
    out=DATA/'dyadic_precision1600_audit_comparison_d138.json';assert not out.exists();start=time.monotonic()
    cert=comparison_review()
    packet={'status':'pass','milestone':'D138','working_precision_pi':1600,
        'production_arithmetic_not_imported':True,'certificates':cert,'wall_seconds':time.monotonic()-start,
        'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
        'sources':[source(p) for p in sorted(USED|{Path(__file__)})]}
    assert packet['peak_rss_bytes']<=2*(1<<30)
    out.write_text(json.dumps(packet,indent=2)+'\n');print(json.dumps(cert),flush=True)
    print('PHASE_METADATA|'+json.dumps(source(out)),flush=True)
    print('PASS|573_DYADIC_PRECISION1600_COMPARISON_AUDIT',flush=True)
