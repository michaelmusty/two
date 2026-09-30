"""D121 independent parameter, interpolation, moment and provenance review."""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import factorial
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
OUT=DATA/'dyadic_schur_review_d121.json'
FP=(2,0,-16,0,20,0,-8,0)
ZERO=(0,)*8;ONE=(1,)+(0,)*7


def read(stem):return json.loads((DATA/(stem+'.json')).read_text())


def source(path):
    path=Path(path).resolve();h=hashlib.sha256()
    with path.open('rb') as f:
        while chunk:=f.read(1<<20):h.update(chunk)
    return {'path':str(path),'sha256':h.hexdigest()}


def checked(rows):
    paths=[]
    for row in rows:
        assert source(row['path'])==row,row['path'];paths.append(Path(row['path']))
    return paths


class Ring:
    def __init__(self,bits):self.mod=1<<bits;self.bits=bits
    def add(self,a,b):return tuple((x+y)%self.mod for x,y in zip(a,b))
    def neg(self,a):return tuple(-x%self.mod for x in a)
    def mul(self,a,b):
        c=[0]*15
        for i,x in enumerate(a):
            for j,y in enumerate(b):c[i+j]+=x*y
        for d in range(14,7,-1):
            for j in range(8):c[d-8+j]-=c[d]*FP[j]
        return tuple(x%self.mod for x in c[:8])
    def rational(self,a,shift=0):
        out=[]
        for value in a:
            x=Q(value)*(1<<shift);assert x.denominator%2
            out.append(x.numerator*pow(x.denominator,-1,self.mod)%self.mod)
        return tuple(out)
    def value(self,a):
        return min([8*self.bits]+[8*((abs(x)&-abs(x)).bit_length()-1)+i for i,x in enumerate(a) if x])


def parameters_review():
    new=read('dyadic_target_transports_d121');old=read('dyadic_moment_transports_refined_d115')
    root=new['root_refinement'];precision=new['parameter_precision_pi'];assert precision==10552
    ring=Ring(root['work_ring_precision_pi']//8)
    x=tuple(map(int,root['new_center']));y=ring.rational(read('definite_dyadic_certificate_d109')['Hensel']['y'])
    residual=ring.add(ring.add(ring.mul(x,x),ring.mul(y,y)),ONE)
    error=ring.value(residual)-ring.value(ring.add(x,x))
    assert ring.value(x)==0 and error==root['new_error_pi']==10816
    assert ring.value(ring.add(x,ring.neg(ring.rational(old['root_refinement']['new_center']))))>=352
    newrows=[c for row in new['transitions'] for c in row['children']]+new['CM_charts']
    oldrows=[c for row in old['transitions'] for c in row['children']]+old['CM_charts']
    checks=[]
    for current,prior,certificate in zip(newrows,oldrows,new['normalization_certificates']):
        assert current['matrix_constant']==prior['matrix_constant'] and current['matrix_slope']==prior['matrix_slope']
        assert current['target_edge']==prior['target_edge']
        shift=certificate['dyadic_common_denominator_bits']
        C=[ring.rational(a,shift) for a in current['matrix_constant']]
        S=[ring.rational(a,shift) for a in current['matrix_slope']]
        V=[ring.add(a,ring.mul(x,b)) for a,b in zip(C,S)]
        vd=ring.value(V[3]);assert vd==certificate['scaled_denominator_valuation_pi']
        norm=[tuple(map(int,a)) for a in current['normalized_center']]
        assert norm[3]==ONE
        # Cross multiplication uses neither pi-division nor unit inversion.
        vals=[ring.value(ring.add(a,ring.neg(ring.mul(z,V[3])))) for a,z in zip(V,norm)]
        assert min(vals)>=precision+vd
        assert min(ring.value(a) for a in V)>=vd
        bound=min(8*ring.bits,error+min(ring.value(a) for a in S))-vd
        assert bound>=precision and current['normalized_error_pi']==precision
        overlap=min(ring.value(ring.add(a,ring.neg(ring.rational(z)))) for a,z in zip(norm,prior['normalized_center']))
        assert overlap>=min(precision,prior['normalized_error_pi'])
        delta=ring.add(norm[0],ring.neg(ring.mul(norm[1],norm[2])))
        assert ring.value(delta)==prior['determinant_valuation']
        assert min(precision,ring.value(norm[2]))==min(precision,prior['denominator_slope_valuation'])
        checks.append(min(vals)-vd)
    assert len(checks)==399
    return {'same_branch_root_error_pi':error,'normalized_maps_cross_multiplied':399,
        'minimum_independent_normalization_error_pi':min(checks),'exported_precision_pi':precision}


def interpolation_review():
    # Ordinary integer monomials span every entry polynomial of a matrix
    # product. Test the exact Newton identity coefficient by coefficient.
    powers=[[1]]
    for j in range(14):
        row=[0]*(len(powers[-1])+1)
        for i,x in enumerate(powers[-1]):row[i]-=j*x;row[i+1]+=x
        powers.append(row)
    for degree in range(15):
        values=[t**degree for t in range(15)];got=[0]*15
        for j in range(15):
            assert values[0]%factorial(j)==0
            c=values[0]//factorial(j)
            for i,x in enumerate(powers[j]):got[i]+=c*x
            values=[b-a for a,b in zip(values,values[1:])]
        assert got==[int(i==degree) for i in range(15)]
    guards=max((factorial(j)&-factorial(j)).bit_length()-1 for j in range(15))
    assert guards==11
    packet=read('dyadic_block_kernel_control_d121')
    assert packet['finite_difference_guard_bits']==guards
    assert packet['field_basis_pair_products_checked']==64
    assert [r['bits'] for r in packet['multiprecision_rectangular_controls']]==[3,25,200,1319,1536]
    return {'exact_integer_monomial_identities':15,'required_interpolation_guard_bits':guards,
        'no_even_ring_element_inverted':True}


def schur_review():
    first=read('dyadic_low_moment_block_d121')
    assert first['graph_profile']['symbolic_block_updates']==2246
    assert first['inverse_verified_in_original_sparse_equations'] and first['actual_harmonic_columns_checked']==16
    small=read('dyadic_schur_iteration_d121')
    assert small['original_operator_final_residual_zero'] and small['exact_overlap_with_entire_frozen_column']
    for r in (8,32,64):
        packet=read(f'dyadic_sparse_low_r{r}_d121')
        assert packet['actual_harmonic_columns_checked']==16
        assert packet['actual_low_scalar_coefficients_checked']==174*r*8*16
        assert packet['unrelated_rhs_scalar_equations_checked']==174*r*8*2
        assert packet['guaranteed_Schur_correction_gain_pi']==r+1
        assert packet['factorization']['block_updates']==2246
    large=read('dyadic_block_schur_r64_d121')
    assert large['successive_correction_gains']==[
        {'before_pi':64,'after_pi':129},{'before_pi':129,'after_pi':194},{'before_pi':194,'after_pi':200}]
    assert large['original_operator_final_residual_zero'] and large['entire_frozen_column_recovered']
    fact=read('dyadic_low_factor_P400_r32_d121')
    assert fact['diagonal_inverse_products_checked']==174 and fact['original_sparse_residual_checked']
    assert fact['binary_payload_bytes']==1226*32*32*8*7
    # All child maps have c and delta in (pi), so a degree-k column lies
    # in (pi^k). Integral low inversion preserves that lower bound.
    pars=read('dyadic_target_transports_d121');ring=Ring(50)
    for row in pars['transitions']:
        for c in row['children']:
            a,b,d=[ring.rational(x) for x in c['normalized_center'][:3]]
            assert ring.value(d)>=1 and ring.value(ring.add(a,ring.neg(ring.mul(b,d))))==1
    return {'low_harmonic_column_checks':16,'full_Schur_column_checks':1,
        'unrelated_factor_rhs_columns':2,'maximum_tested_gain_pi':65,
        'actual_P400_factor_dimension':174*32,'unit_low_inversion_and_column_divisibility_checked':True}


def read_binary(path,nr,nc,bits):
    width=(bits+7)//8;raw=path.read_bytes();assert len(raw)==nr*nc*8*width
    return [[tuple(int.from_bytes(raw[((i*nc+j)*8+k)*width:((i*nc+j)*8+k+1)*width],'little')
                   for k in range(8)) for j in range(nc)] for i in range(nr)]


def actual_review():
    packet=read('dyadic_actual_P400_col0_verified_d121')
    assert packet['certificate']['original_full_residual_zero']
    assert packet['certificate']['actual_new_precision_pi']==400 and packet['harmonic_basis_column']==0
    assert packet['residual_lower_bound_pi']==400 and packet['actual_moment_precision_increased']
    state=read_binary(DATA/'dyadic_actual_P400_col0_verified_d121_state.bin',174,400,50)
    zero=read_binary(DATA/'dyadic_actual_P400_col0_verified_d121_residual.bin',174,400,50)
    assert all(x==ZERO for row in zero for x in row)
    old=read('dyadic_precision200_d115');mask=(1<<25)-1
    assert [[tuple(c&mask for c in x) for x in row] for row in state]==[
        [tuple(m[0]) for m in row[:400]] for row in old['state_moments_power_basis']]
    # Independently evaluate selected original equations with the direct
    # phi^n coefficient recurrence, avoiding generating functions and LU.
    maps=read('dyadic_target_transports_d121')['transitions'];ring=Ring(50)
    degrees=(1,2,33,64);count=0
    for e in (0,17,61,98,173):
        totals={n:ZERO for n in degrees}
        for child in maps[e]['children']:
            a,b,c=[ring.rational(x) for x in child['normalized_center'][:3]]
            powers=[ONE]+[ZERO]*399;moments=state[child['target_edge']]
            for n in range(1,max(degrees)+1):
                nextrow=[ring.mul(b,powers[0])]
                for k in range(1,400):
                    nextrow.append(ring.add(ring.add(ring.mul(b,powers[k]),ring.mul(a,powers[k-1])),
                                            ring.neg(ring.mul(c,nextrow[-1]))))
                powers=nextrow
                if n in degrees:
                    total=ZERO
                    for x,y in zip(powers,moments):total=ring.add(total,ring.mul(x,y))
                    totals[n]=ring.add(totals[n],total)
        for n in degrees:assert totals[n]==state[e][n];count+=8
        print(f'INDEPENDENT_ACTUAL_RESIDUAL|state={e}; checked={count}',flush=True)
    return {'actual_precision_pi':400,'actual_harmonic_columns_refined':1,
        'entire_original_residual_scalar_checks_in_driver':174*400*8,
        'independent_recurrence_scalar_checks':count,'independent_output_degrees':list(degrees),
        'P200_overlap_scalar_checks':174*400*8,'full_sixteen_column_bank_precision_pi':200}


def CM_review():
    packet=read('dyadic_actual_CM_P400_col0_d121')
    assert packet['harmonic_basis_column']==0 and packet['coarse_error_beta']==[832,848,832,864]
    moments=read_binary(DATA/'dyadic_actual_CM_P400_col0_d121_moments.bin',17,800,50)
    # Derive the beta polynomial from f(-2-beta^2), independently of its
    # hard-coded coefficient list, then use Horner kernel evaluation.
    mp=[0]*17;power=[1]
    for degree,c in enumerate(list(FP)+[1]):
        for i,x in enumerate(power):mp[i]+=c*x
        nxt=[0]*(len(power)+2)
        for i,x in enumerate(power):nxt[i]-=2*x;nxt[i+2]-=x
        power=nxt
    assert mp==[int(x) for x in read('dyadic_poisson_jet_interface_d108')['CM_polynomial_ascending']]
    class CM(Ring):
        def mul(self,a,b):
            out=[0]*31
            for i,x in enumerate(a):
                for j,y in enumerate(b):out[i+j]+=x*y
            for d in range(30,15,-1):
                for j in range(16):out[d-16+j]-=out[d]*mp[j]
            return tuple(x%self.mod for x in out[:16])
        def value(self,x):return min([864]+[16*((c&-c).bit_length()-1)+i for i,c in enumerate(x) if c])
        def scale(self,x,n):return tuple(c*n%self.mod for c in x)
    cm=CM(54);z=(0,)*16;one=(1,)+(0,)*15;beta=(0,1)+(0,)*14
    pi=cm.add(cm.scale(cm.mul(beta,beta),-1),cm.scale(one,-2))
    qp=cm.add(tuple(mp[1:]),cm.neg(beta));assert cm.mul(beta,qp)==pi
    powers=[one]
    for _ in range(7):powers.append(cm.mul(powers[-1],pi))
    from math import comb
    coefficients=[]
    for order in range(4):
        n=2*order+2
        coefficients.append([2*sum((-2)**k*comb(n,k+1)*comb(k+r,r) for k in range(n)) for r in range(800)])
    for ci,chart in enumerate(moments):
        embedded=[]
        for row in chart:
            x=z
            for c,a in zip(row,powers):x=cm.add(x,cm.scale(a,c))
            embedded.append(x)
        for order,cs in enumerate(coefficients):
            value=z
            for c,x in reversed(list(zip(cs,embedded))):value=cm.add(cm.mul(value,qp),cm.scale(x,c))
            assert value==tuple(packet['CM_values'][ci]['coarse_coefficients_beta'][order])
    return {'actual_harmonic_columns_refined':1,'CM_chart_precision_pi':400,
        'independent_coarse_values_checked':68,'method':'alternate binomial kernel and Horner evaluation',
        'coarse_error_beta':[832,848,832,864]}


def calculations():
    result={'parameters':parameters_review(),'interpolation':interpolation_review(),
            'Schur':schur_review(),'actual_moments':actual_review(),'actual_CM':CM_review()}
    print('SCHUR_REVIEW|independent parameter, interpolation and actual-moment checks pass',flush=True)
    return result


def build(certificate):
    priorpath=DATA/'construction_reassessment_review_d120.json';prior=json.loads(priorpath.read_text())
    assert prior['status']=='pass' and len(prior['sources'])==961
    paths=checked(prior['sources'])+[priorpath,Path(__file__),
        ROOT/'dembele/certificates/dyadic-schur-lift-d121.md',DATA/'dyadic_schur_sources_d121.json']
    jobs=[]
    for path in sorted(DATA.glob('*d121*')):
        if path.name.startswith('dyadic_schur_review_d121'):continue
        paths.append(path)
        if path.suffix!='.json':continue
        packet=json.loads(path.read_text())
        paths += checked([x for x in packet.get('sources',[]) if isinstance(x,dict) and 'sha256' in x])
        paths += checked(packet.get('checkpoint_files',[]))
        if path.name.endswith('.job.json'):
            assert packet['timeout_seconds']==180 and packet['timeout_terminates_process_group']
            paths += checked([packet['log']])
            if packet['status']=='pass':paths += checked([packet['driver']])
            else:
                assert packet['status']=='failed';snap=packet['failed_driver_snapshot'];paths += checked([snap])
                assert snap['sha256']==packet['driver']['sha256']
            jobs.append({'receipt':path.name,'status':packet['status'],'wall_seconds':packet['wall_seconds']})
    return {'status':'pass','milestone':'D121','D120_source_hashes_checked_unchanged':961,
        'certificate':certificate,'bounded_input_jobs':jobs,
        'actual_harmonic_column0_low_moment_precision_pi':400,'full_sixteen_column_bank_precision_pi':200,
        'transport_parameter_precision_pi':10552,'large_target_precision_solver_ready':False,
        'positive_quadric_jet_exact_vanishing_proved':False,'candidate_identification_proved':False,
        'target_field_polynomial_constructed':False,
        'sources':[source(path) for path in sorted(set(p.resolve() for p in paths))]}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--probe',action='store_true')
    parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result=calculations()
    if not args.probe:
        result=build(result)
        if args.check:
            previous=json.loads(OUT.read_text());checked(previous['sources']);assert previous==result
        else:
            assert not OUT.exists();OUT.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'sources':len(result['sources']),'input_jobs':len(result['bounded_input_jobs'])}),flush=True)
    print('PASS|474_DYADIC_SCHUR_REVIEW',flush=True)
