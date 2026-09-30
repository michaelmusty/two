"""D114 independent moment and coarse-Poisson review.

Ordinary coefficient arithmetic checks the optimized moment bank. Independent
expansion of (1-((beta+t)/(beta-t))^(2j+2))/2 checks the coarse kernels.
The CM involution supplies a second, stronger enclosure using twice chart A.
"""
import argparse
from functools import lru_cache
import importlib.util
import json
from math import comb
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
OUT=DATA/'dyadic_coarse_review_d114.json';REPORT=ROOT/'dembele/certificates/dyadic-coarse-d114.md'
spec=importlib.util.spec_from_file_location('rational',ROOT/'dembele/pari/399_definite_dyadic_review.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
source,checked=r.source,r.checked
FZ=(0,)*8;FO=(1,)+(0,)*7
MP=[2,0,64,0,336,0,672,0,660,0,352,0,104,0,16,0,1]
MZ=(0,)*16;MO=(1,)+(0,)*15;BETA=(0,1)+(0,)*14

def fenc(x):return tuple(int(c.numerator*pow(c.denominator,-1,4)%4) for c in map(r.Q,x))
def fadd(x,y):return tuple((a+b)%4 for a,b in zip(x,y))
def fscale(x,c):return tuple(a*c%4 for a in x)
@lru_cache(maxsize=65536)
def fmul(x,y):
    z=np.convolve(x,y);z[:7]-=2*z[8:15]
    return tuple(int(c)%4 for c in z[:8])
def fpowers(x,n):
    ans=[FO]
    for _ in range(n):ans.append(fmul(ans[-1],x))
    return ans
def fval(x):return min((i+(8 if c%2==0 else 0) for i,c in enumerate(x) if c),default=16)
@lru_cache(None)
def fmatrix(x):
    out=np.zeros((8,8),dtype=np.int64)
    for i,c in enumerate(x):
        for j in range(8):out[(i+j)%8,j]+=c*(-2 if i+j>=8 else 1)
    return out
def params(row):return tuple(fenc(x) for x in row['normalized_center'][:3])
@lru_cache(None)
def rational_powers(p,degree,cutoff):
    # Independent numerator binomial / denominator binomial expansion.
    aa,bb,cc=p;ap,bp,cp=fpowers(aa,degree),fpowers(bb,degree),fpowers(cc,min(15,cutoff))
    rows=[[FO]+[FZ]*cutoff]
    for n in range(1,degree+1):
        numerator=[fscale(fmul(ap[i],bp[n-i]),comb(n,i)%4) for i in range(min(n,cutoff)+1)]
        denominator=[fscale(cp[k],((-1)**k*comb(n+k-1,k))%4) for k in range(len(cp))]
        row=[FZ]*(cutoff+1)
        for i,a in enumerate(numerator):
            if a!=FZ:
                for k,b in enumerate(denominator[:cutoff+1-i]):
                    if b!=FZ:row[i+k]=fadd(row[i+k],fmul(a,b))
        rows.append(row)
    return rows

def moments_check(packet):
    assert [packet[k] for k in ['working_precision_pi','low_cutoff','state_cutoff','CM_cutoff','iterations']]==[16,15,46,31,16]
    transport=json.loads((DATA/'dyadic_moment_transports_d113.json').read_text())
    harmonic=json.loads((DATA/'dyadic_harmonic_certificate_d111.json').read_text())
    old=json.loads((DATA/'dyadic_moment_pilot_d113.json').read_text())
    bank=np.array(packet['state_moments_power_basis'],dtype=np.int64).transpose(0,1,3,2)
    assert bank.shape==(174,47,8,16) and np.all((bank>=0)&(bank<4))
    basis=[tuple(r.Q(i==j) for i in range(8)) for j in range(8)]
    assert all(fmul(fenc(x),fenc(y))==fenc(r.mul(x,y)) for x in basis for y in basis)
    for e,row in enumerate(transport['transitions']):
        rhs=np.zeros((47,8,16),dtype=np.int64)
        for child in row['children']:
            assert child['normalized_error_pi']>=16
            cs=rational_powers(params(child),46,16)
            for n in range(47):
                assert cs[n][16]==FZ
                for k,c in enumerate(cs[n][:16]):
                    if n and k:assert fval(c)>=k
                    if c!=FZ:rhs[n]+=fmatrix(c)@bank[child['target_edge'],k]
        assert np.array_equal(rhs%4,bank[e]),f'moment residual {e}'
        expected=np.zeros((8,16),dtype=np.int64);expected[0]=[x[e]%4 for x in harmonic['harmonic_basis']]
        assert np.array_equal(bank[e,0],expected)
    mod12=np.array([4]*4+[2]*4,dtype=np.int64)
    assert np.array_equal(bank[:,:12]%mod12[None,None,:,None],
                          np.array(old['state_moments_power_basis']).transpose(0,1,3,2))
    assert len(packet['CM_chart_moments'])==51
    for index,(row,saved) in enumerate(zip(transport['CM_charts'],packet['CM_chart_moments'])):
        assert (row['CM_index'],row['chart'])==(saved['CM_index'],saved['chart'])
        assert saved['error_pi']==16 and row['normalized_error_pi']>=16
        cs=rational_powers(params(row),31,46);rhs=np.zeros((32,8,16),dtype=np.int64)
        for n in range(32):
            for k,c in enumerate(cs[n]):
                assert fval(c)>=min(16,max(0,k-n))
                if c!=FZ:rhs[n]+=fmatrix(c)@bank[row['target_edge'],k]
        assert np.array_equal(rhs%4,np.array(saved['moments_power_basis']).transpose(0,2,1))
        assert saved['zeroth_moments_exact']==row['zeroth_moments']
    print('MOMENT_REVIEW|130848 state entries and 26112 CM entries; all residuals and transfers exact modulo pi^16',flush=True)
    return {'state_entries':174*47*16,'CM_moment_entries':51*32*16,
            'moment_precision_pi':16,'higher_rows_verified':31,
            'column_16_vanishes':True,'D113_overlap_checked':True}

class FieldQuotient:
    # Separate list-based integer arithmetic using the full CM polynomial.
    def __init__(self,precision):
        self.precision=precision;self.mods=[1<<max(0,(precision-i+15)//16) for i in range(16)]
        self.maximum=max(self.mods)
    def norm(self,x):return tuple(int(c)%m for c,m in zip(x,self.mods))
    def add(self,x,y):return self.norm([a+b for a,b in zip(x,y)])
    def scale(self,x,c):return self.norm([a*c for a in x])
    @lru_cache(maxsize=32768)
    def mul(self,x,y):
        v=[0]*31
        for i,a in enumerate(x):
            if a:
                for j,b in enumerate(y):
                    if b:v[i+j]+=a*b
        for k in range(30,15,-1):
            c=v[k]%self.maximum
            if c:
                for j,d in enumerate(MP[:-1]):
                    if d:v[k-16+j]-=c*d
        return self.norm(v[:16])
    def powers(self,x,n):
        ans=[MO]
        for _ in range(n):ans.append(self.mul(ans[-1],x))
        return ans
    def val(self,x):return min((16*((int(c)&-int(c)).bit_length()-1)+i for i,c in enumerate(x) if c),default=self.precision)
    @lru_cache(None)
    def matrix(self,x):
        return np.array([self.mul(x,tuple(int(i==j) for i in range(16))) for j in range(16)],dtype=np.int64).T

def independent_kernels():
    # The temporary extra 16 beta-digits account for division by 2.
    work=FieldQuotient(96);out=FieldQuotient(80)
    pi=work.add(work.scale(work.mul(BETA,BETA),-1),work.scale(MO,-2))
    qA=work.add(work.norm(MP[1:]),work.scale(BETA,-1));qC=work.mul(BETA,pi)
    assert work.mul(qA,BETA)==pi
    bp=work.powers(BETA,96);inverse=MZ
    for x in bp[:-1]:inverse=work.add(inverse,work.scale(x,-1))
    assert bp[-1]==MZ and work.mul(work.add(BETA,work.scale(MO,-1)),inverse)==MO
    U=work.add(BETA,MO);Up=work.powers(U,6);Vp=work.powers(inverse,37)
    Ap,Cp,pip=work.powers(qA,31),work.powers(qC,31),work.powers(pi,31)
    fpoly=[2,0,-16,0,20,0,-8,0,1];value=MZ
    for c in reversed(fpoly):value=work.add(work.mul(value,pi),work.scale(MO,c))
    assert value==MZ
    def half(x):
        assert all(c%2==0 for c in x)
        return out.norm([c//2 for c in x])
    bank=[]
    for j in range(3):
        n=2*j+2;rows=[[],[],[]]
        for degree in range(32):
            count=sum(comb(n,i)*comb(n+degree-i-1,degree-i) for i in range(min(n,degree)+1))
            rows[0].append(MZ if degree==0 else half(work.scale(Ap[degree],-count)))
            acc=MZ
            for i in range(min(n,degree)+1):
                c=comb(n,i)*comb(n+degree-i-1,degree-i)
                acc=work.add(acc,work.scale(work.mul(Up[n-i],Vp[n+degree-i]),c))
            coefficient=work.mul(pip[degree],acc)
            numerator=work.add(MO,work.scale(coefficient,-1)) if degree==0 else work.scale(coefficient,-1)
            rows[1].append(half(numerator))
            rows[2].append(MZ if degree==0 else half(work.scale(Cp[degree],-count)))
        bank.append(rows)
    assert work.val(work.scale(MO,2))==16
    return bank,out,out.norm(pi)

def poisson_checks(moments,coarse):
    assert coarse['arithmetic_precision_beta']==80 and coarse['coarse_error_beta']==[48,64,48]
    kernels,ring,pi=independent_kernels()
    assert kernels==[[[tuple(x) for x in row] for row in group] for group in coarse['kernel_coefficients_beta']]
    gains=[]
    for j in range(3):
        values=[16*(k+(comb(2*j+2,k+1)&-comb(2*j+2,k+1)).bit_length()-1) for k in range(2*j+2)]
        gains.append(values)
    assert gains==coarse['binomial_error_gains_beta']
    assert [32+min(x) for x in gains]==[48,64,48]
    embed=np.array(ring.powers(pi,7),dtype=np.int64);mods=np.array(ring.mods,dtype=np.int64)
    raw=np.array([row['moments_power_basis'] for row in moments['CM_chart_moments']],dtype=np.int64)
    bank=((raw@embed)%mods).reshape(17,3,32,16,16).transpose(0,1,2,4,3)
    refined=[];counts=[0]*3;refined_counts=[0]*3;errors=[64,80,64]
    for ci in range(17):
        values=[];valuations=[];lower=[]
        for j in range(3):
            answer=np.zeros((16,16),dtype=np.int64);only_A=np.zeros((16,16),dtype=np.int64)
            for chart in range(3):
                for degree,c in enumerate(kernels[j][chart]):
                    if c!=MZ:
                        term=ring.matrix(c)@bank[ci,chart,degree];answer+=term
                        if chart==0:only_A+=2*term
            answer%=mods[:,None];only_A%=mods[:,None]
            saved=coarse['CM_values'][ci]
            assert np.array_equal(answer.T,np.array(saved['coarse_coefficients_beta'][j]))
            vs=[ring.val(tuple(x)) for x in answer.T]
            assert [v if v<coarse['coarse_error_beta'][j] else None for v in vs]==saved['certified_valuations_beta'][j]
            counts[j]+=sum(v<coarse['coarse_error_beta'][j] for v in vs)
            difference=(answer-only_A)%mods[:,None]
            assert all(ring.val(tuple(x))>=coarse['coarse_error_beta'][j] for x in difference.T)
            rv=[ring.val(tuple(x)) for x in only_A.T]
            values.append(only_A.T.tolist());valuations.append([v if v<errors[j] else None for v in rv])
            lower.append([min(v,errors[j]) for v in rv]);refined_counts[j]+=sum(v<errors[j] for v in rv)
        refined.append({'CM_index':ci,'coarse_coefficients_beta':values,'error_beta':errors,
                        'certified_valuations_beta':valuations,'valuation_lower_bounds_beta':lower})
    assert counts==coarse['nonzero_entries_by_coarse_order']==[250,250,250]
    assert coarse['anchor_nonvanishing_witness'] is None
    # Each 2*S_A(j,r) is divisible by 4,8,4 respectively, uniformly in r.
    coefficient_v2=[]
    for j in range(3):
        n=2*j+2;coeff=[2*(-2)**k*comb(n,k+1) for k in range(n)]
        vv=min((abs(c)&-abs(c)).bit_length()-1 for c in coeff)
        coefficient_v2.append(vv);assert sum(coeff)==0
    assert coefficient_v2==[2,3,2]
    assert errors==[32+16*v for v in coefficient_v2]
    assert all(x is None for row in refined[0]['certified_valuations_beta'] for x in row)
    # Anchor chart A moments of degrees 0..31 all vanish modulo pi^16.
    assert np.all(raw[0]==0)
    # (X^2-X)^16 is a monic integral polynomial of degree 32, taking values
    # in pi^16 O_K on O_K. Monic division then proves every polynomial
    # moment at the anchor is divisible by pi^16, at any degree.
    null_poly=[0]*33
    for k in range(17):null_poly[16+k]=comb(16,k)*(-1)**(16-k)
    assert null_poly[-1]==1 and null_poly[0]==0
    anchor_lower=[32+1+16*v for v in coefficient_v2]
    wrong=ring.scale(kernels[0][2][1],-1)
    assert ring.val(ring.add(wrong,ring.scale(kernels[0][2][1],-1)))<80
    print(f'POISSON_REVIEW|independent rational kernels; refined errors {errors}; nonzero {refined_counts}',flush=True)
    print(f'ANCHOR_BOUND|all polynomial A moments divisible by pi^16; coarse beta-valuations >= {anchor_lower}',flush=True)
    return {'kernel_identity_independently_checked':True,'temporary_division_precision_beta':96,
            'raw_errors_beta':[48,64,48],'raw_nonzero_counts':counts,
            'symmetry_refined_errors_beta':errors,'symmetry_refined_nonzero_counts':refined_counts,
            'symmetry_refined_CM_values':refined,'three_chart_and_twice_A_enclosures_agree':True,
            'wrong_infinity_kernel_sign_rejected':True,
            'anchor_all_polynomial_A_moments_divisible_pi16':True,
            'anchor_monic_null_polynomial':null_poly,'anchor_coarse_lower_bounds_beta':anchor_lower,
            'anchor_nonvanishing_certified':False,'normalization_performed':False}

def computations():
    moments=json.loads((DATA/'dyadic_moment_extension_d114.json').read_text())
    coarse=json.loads((DATA/'dyadic_coarse_poisson_d114.json').read_text())
    return {'moments':moments_check(moments),'Poisson':poisson_checks(moments,coarse)}

def build():
    result=computations();previous=DATA/'dyadic_moment_review_d113.json'
    prior=json.loads(previous.read_text());assert prior['status']=='pass' and len(prior['sources'])==696
    paths=checked(prior['sources'])+[previous,Path(__file__),REPORT,DATA/'dyadic_coarse_sources_d114.json']
    for name in ['dyadic_moment_extension_d114.json','dyadic_coarse_poisson_d114.json']:
        p=DATA/name;record=json.loads(p.read_text());paths+=[p]+checked(record['sources'])
    for pattern in ['dyadic_moment_extension_d114_attempt*.job.json','dyadic_coarse_poisson_d114_attempt*.job.json',
                    'dyadic_coarse_review_d114_probe_attempt*.job.json']:
        for p in sorted(DATA.glob(pattern)):
            job=json.loads(p.read_text());assert job['timeout_seconds']==180 and job['timeout_terminates_process_group']
            paths+=[p]+checked(job['sources']+[job['log']])
            if job['status']=='pass':
                assert job['wall_seconds']<180;paths+=checked([job['driver']])
            else:
                assert job['status'] in ['failed','timeout']
                snapshot=p.with_name(p.name.replace('.job.json','_failed'+Path(job['driver']['path']).suffix))
                assert source(snapshot)['sha256']==job['driver']['sha256'];paths.append(snapshot)
    return {'status':'pass','milestone':'D114','certificates':result,'D113_source_hashes_checked_unchanged':696,
            'actual_harmonic_coarse_differential_2jet_computed':True,
            'actual_rational_frame_ratio_jet_computed':False,'actual_harmonic_to_residue_frame_change_computed':False,
            'anchor_nonvanishing_certified':False,'Gaussian_pivot_certified':False,
            'candidate_identification_proved':False,'target_field_polynomial_constructed':False,
            'sources':[source(p) for p in sorted(set(p.resolve() for p in paths))]}

def main():
    parser=argparse.ArgumentParser(description=__doc__);g=parser.add_mutually_exclusive_group()
    g.add_argument('--probe',action='store_true');g.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.probe:
        result=computations();p=result['Poisson']
        print(json.dumps({'moments':result['moments'],'refined_errors_beta':p['symmetry_refined_errors_beta'],
                         'refined_nonzero_counts':p['symmetry_refined_nonzero_counts'],
                         'anchor_lower_bounds_beta':p['anchor_coarse_lower_bounds_beta']},indent=2),flush=True)
        print('PASS|D114_COARSE_PROBE',flush=True);return
    if args.check:old=json.loads(OUT.read_text());checked(old['sources'])
    result=build()
    if args.check:assert result==old
    else:
        assert not OUT.exists();OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'pass','source_hashes':len(result['sources']),'D113_hashes_unchanged':696}),flush=True)
    print('PASS|D114_COARSE_REVIEW',flush=True)

if __name__=='__main__':main()
