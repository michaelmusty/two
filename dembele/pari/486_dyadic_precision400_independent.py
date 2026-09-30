"""D122 independent, bounded arithmetic reviews of the complete P=400 bank.

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


def binary(path,nr,nc):
    path=Path(path);USED.add(path);raw=path.read_bytes();width=7
    assert len(raw)==nr*nc*8*width
    return [[tuple(int.from_bytes(raw[((i*nc+j)*8+k)*width:((i*nc+j)*8+k+1)*width],'little')
                   for k in range(8)) for j in range(nc)] for i in range(nr)]


def roots_review():
    packet=read('dyadic_CM_frame_beta21168_d122')
    old=read('dyadic_cm_matching_review_d112')['certificates']['roots_and_frame']
    proposals=read('dyadic_cm_root_proposals_d112')
    basis=read('cm_field_recognition')['field_basis']['trace_centered_basis_power_coordinates'][1:]
    assert list(MP)==packet['CM_polynomial'] and packet['root_polynomial']==proposals['root_polynomial']
    assert packet['CM_point_root_matching']==old['CM_point_root_matching']
    ring=Quotient(MP,packet['work_precision_beta']);export=packet['rational_residue_frame_error_beta']
    poly=packet['root_polynomial'];derivative=[i*poly[i] for i in range(1,len(poly))]
    roots=[ring.norm(row) for row in packet['root_centers']];errors=[]
    for i,x in enumerate(roots):
        residual=ring.value(ring.evaluate(poly,x));d=ring.value(ring.evaluate(derivative,x))
        assert residual>2*d
        error=residual-d;row=packet['root_certificates'][i]
        assert error==row['new_error_beta'] and d==row['derivative_valuation_beta']
        overlap=ring.value(ring.sub(x,ring.rational(proposals['root_centers'][i])))
        assert overlap>=old['root_certificates'][i]['root_error_valuation_beta']>old['maximum_root_separation_valuation_beta']
        errors.append(error)
    minimum=ring.precision;checks=0
    for point,matching in enumerate(packet['CM_point_root_matching']):
        index=matching['dyadic_root_index'];x=roots[index]
        for j,row in enumerate(basis):
            rational=list(map(Q,row));den=lcm(*(c.denominator for c in rational))
            coeff=[int(c*den) for c in rational];vd=16*((den&-den).bit_length()-1)
            saved=ring.norm(packet['rational_residue_frame_values'][point][j])
            residual=ring.value(ring.sub(ring.evaluate(coeff,x),ring.scale(saved,den)))
            assert residual>=export+vd and errors[index]-vd>=export
            minimum=min(minimum,residual-vd,errors[index]-vd);checks+=1
    out=Quotient(MP,export)
    for j in range(16):
        total=out.zero
        for row in packet['rational_residue_frame_values']:total=out.add(total,out.norm(row[j]))
        assert total==out.zero
    assert checks==272 and minimum>=21168
    return {'root_residuals_and_original_branches_checked':17,'eta_values_cross_multiplied':checks,
        'eta_error_beta':export,'minimum_independent_eta_bound_beta':minimum,
        'trace_centered_sums_checked':16,'production_Hensel_division_not_reused':True}


def moments_review():
    bank=read('dyadic_precision400_d122');old=read('dyadic_precision200_d115')
    harmonic=read('dyadic_harmonic_certificate_d111')['harmonic_basis']
    maps=read('dyadic_target_transports_d121')['transitions']
    ring=Quotient(FP,400);degrees=(1,2,33,64);states=(0,17,61,98,173)
    kernels={}
    for e in states:
        for branch,child in enumerate(maps[e]['children']):
            a,b,c=[ring.norm(x) for x in child['normalized_center'][:3]]
            power=[ring.one]+[ring.zero]*399
            for n in range(1,max(degrees)+1):
                row=[ring.mul(b,power[0])]
                for k in range(1,400):
                    row.append(ring.sub(ring.add(ring.mul(b,power[k]),ring.mul(a,power[k-1])),ring.mul(c,row[-1])))
                power=row
                if n in degrees:kernels[e,branch,n]=row
    checked=0;overlap=0;mask=(1<<25)-1
    for col,record in enumerate(bank['state_columns']):
        meta=read(Path(record['verified_state_metadata']['path']).stem)
        assert meta['certificate']['original_full_residual_zero']
        assert meta['certificate']['scalar_coefficients_checked']==174*400*8
        if col:assert meta['certificate']['full_residual_uses_different_polynomial_backend_from_lift']
        state=binary(record['state_binary']['path'],174,400)
        residual=Path(meta['checkpoint_files'][1]['path']);USED.add(residual)
        raw=residual.read_bytes();assert len(raw)==174*400*8*7 and not any(raw)
        for e,row in enumerate(state):
            assert row[0]==(harmonic[col][e]&ring.mask,)+(0,)*7
            for k,m in enumerate(row):
                assert tuple(c&mask for c in m)==tuple(old['state_moments_power_basis'][e][k][col])
                overlap+=8
        for e in states:
            for n in degrees:
                total=ring.zero
                for branch,child in enumerate(maps[e]['children']):
                    moments=state[child['target_edge']]
                    for coefficient,m in zip(kernels[e,branch,n],moments):
                        total=ring.add(total,ring.mul(coefficient,m))
                assert total==state[e][n],(col,e,n);checked+=8
        print(f'INDEPENDENT_STATE_COLUMN|{col}; recurrence scalars={checked}',flush=True)
    assert overlap==8908800 and checked==2560
    return {'actual_columns':16,'precision_pi':400,'all_old_low_state_scalar_overlaps_checked':overlap,
        'independent_original_recurrence_scalar_checks':checked,'sample_states':list(states),'sample_degrees':list(degrees),
        'production_full_original_residual_scalar_checks':8908800,'all_saved_full_residuals_zero':True}


def coarse_review(first,last):
    assert 0<=first<=last<16
    bank=read('dyadic_precision400_d122');ring=Quotient(MP,864)
    pi=ring.sub(ring.scale(ring.one,-2),ring.mul(ring.beta,ring.beta))
    q=ring.sub(tuple(MP[1:]),ring.beta);assert ring.mul(q,ring.beta)==pi and ring.value(q)==1
    powers=[ring.one]
    for _ in range(7):powers.append(ring.mul(powers[-1],pi))
    coefficients=[]
    for order in range(4):
        n=2*order+2
        # Coefficients of -(1+X)^n/(1-X)^n, with constant cancelled.
        coefficients.append([0]+[-sum(comb(n,i)*comb(n+r-i-1,r-i) for i in range(min(n,r)+1)) for r in range(1,800)])
    checks=0
    for col in range(first,last+1):
        stem='dyadic_actual_CM_P400_col0_d121' if col==0 else f'dyadic_actual_CM_P400_col{col:02d}_d122'
        packet=read(stem);moments=binary(DATA/(stem+'_moments.bin'),17,800)
        assert packet['coarse_error_beta']==bank['coarse_error_beta']==[832,848,832,864]
        for ci,chart in enumerate(moments):
            embedded=[]
            for m in chart:
                x=ring.zero
                for c,p in zip(m,powers):x=ring.add(x,ring.scale(p,c))
                embedded.append(x)
            for order,cs in enumerate(coefficients):
                x=ring.zero
                for c,m in reversed(list(zip(cs,embedded))):x=ring.add(ring.mul(x,q),ring.scale(m,c))
                assert x==tuple(packet['CM_values'][ci]['coarse_coefficients_beta'][order])
                assert x==tuple(bank['CM_values'][ci]['coarse_coefficients_beta'][order][col])
                checks+=1
        print(f'INDEPENDENT_COARSE_COLUMN|{col}; values={checks}',flush=True)
    return {'first_column':first,'last_column':last,'coarse_values_checked':checks,
        'coarse_error_beta':[832,848,832,864],'method':'separate quotient Horner product and binomial-series kernel'}


def comparison_review():
    bank=read('dyadic_precision400_d122');frame=read('dyadic_residue_frame400_d122')
    eta=read('dyadic_CM_frame_beta21168_d122');candidate=read('cm_frame_curve_candidate')
    quadrics=read('dyadic_integral_quadrics400_d122');old=read('dyadic_precision200_d115')
    design=read('dyadic_precision_design_d120')['precision_design']
    budget=read('cm_arithmetic_height_budget_d118')['budgets']
    ring=Quotient(MP,2048)

    class Ball:
        def __init__(self,x=None,error=2048):
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
        if v is None:return Ball(error=2048 if exact else row['error_beta']+shift)
        assert v+shift>=0
        return Ball(ring.mul(ring.norm(row['unit_beta']),ring.power_beta(v+shift)),
                    2048 if exact else row['error_beta']+shift)
    def dot(xs,ys):
        value=Ball()
        for x,y in zip(xs,ys):value=value+x*y
        return value
    def check_enclosure(value,record):
        expected=saved(record)
        assert not(value-expected).nonzero()
        assert value.error>=record['error_beta'],(value.error,record['error_beta'])
        assert value.lower()>=expected.lower()

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
    etaballs=[[Ball(x,1024) for x in row] for row in eta['rational_residue_frame_values']]
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
    return {'frame_relation_certified_error_beta':qbound,'change_column_error_bounds_beta':change_bounds,
        'inherited_inverse_norm_preserved_by_overlap_beta':min(overlap),'all_actual_jet_values_checked':17*4*16,
        'independent_quadric_coefficients_checked':counts,'positive_coefficients_checked':4641,
        'certified_mismatch_count':len(mismatches),'degree16_section_lower_beta':[min(x[n] for x in minimums[1:]) for n in (1,2,3)],
        'anchor_section_lower_beta':minimums[0][1:],'sufficient_nonanchor_beta':thresholds,
        'W_Gaussian':gaussians[0],'W_Gaussian_inverted':False,'positive_exact_vanishing_proved':False,
        'method':'integer quotient absolute-error balls, frame residual bounds, gradients and polar forms'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase',choices=['roots','moments','coarse','comparison'])
    parser.add_argument('--first',type=int,default=0);parser.add_argument('--last',type=int,default=3)
    parser.add_argument('--probe',action='store_true');args=parser.parse_args()
    suffix=args.phase+(f'_{args.first:02d}_{args.last:02d}' if args.phase=='coarse' else '')
    out=DATA/f'dyadic_precision400_audit_{suffix}_d122.json'
    if not args.probe:assert not out.exists()
    if args.phase=='roots':result=roots_review()
    elif args.phase=='moments':result=moments_review()
    elif args.phase=='coarse':result=coarse_review(args.first,args.last)
    else:result=comparison_review()
    packet={'status':'pass','milestone':'D122','phase':suffix,'certificates':result,
        'sources':[source(p) for p in sorted(USED|{Path(__file__)})]}
    if not args.probe:out.write_text(json.dumps(packet,indent=2)+'\n')
    print(json.dumps(result),flush=True)
    print('PASS|486_DYADIC_PRECISION400_INDEPENDENT',flush=True)
