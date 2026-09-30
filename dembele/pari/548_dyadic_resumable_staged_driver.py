"""D132 separately capped, resumable weighted staged refinement phases.

The scheduler is nonmathematical. Each invocation commits one bounded job;
committed rows and jobs survive a missing receipt. Only the owned working
store is mutable. Current arithmetic uses the original GMP operator.
"""
import argparse
import hashlib
import importlib.util
import json
from math import comb
import os
from pathlib import Path
import resource
import sys
import time
import types

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
def module(name,file):
    s=importlib.util.spec_from_file_location(name,ROOT/'dembele/pari'/file)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
j=module('store','547_dyadic_staged_store.py')
v=module('weighted','541_dyadic_weighted_certificate.py')
coarse=module('coarse','475_dyadic_actual_CM_column.py')
b,l,p,c=v.b,v.l,v.p,v.w.c
N,R=174,32
CACHE={}
def source(path):
    path=Path(path).resolve()
    if path not in CACHE:
        sha=hashlib.sha256()
        with path.open('rb') as f:
            while raw:=f.read(1<<20):sha.update(raw)
        CACHE[path]={'path':str(path),'sha256':sha.hexdigest()}
    return CACHE[path]
c.h.source=source

def read(stem):
    d=json.loads((DATA/(stem+'.json')).read_text());assert d['status']=='pass';return d

def decode(raw,count,bits,weighted=False):
    if not weighted:
        row=b.unpack(raw,1,count,bits)[0]
        assert all(0<=x<1<<bits for t in row for x in t);return row
    out=[];at=0
    for bs in v.layout(count,bits,True):
        row=[]
        for bit in bs:
            width=(bit+7)//8;x=int.from_bytes(raw[at:at+width],'little');at+=width
            assert x<1<<bit;row.append(x)
        out.append(tuple(row))
    assert at==len(raw);return out

def low_decode(raw,bits):return [[x] for x in decode(raw,R,bits)]
def low_pack(edge,bits):return b.pack(edge,bits)
def peak():return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)

def immutable_dependencies():
    paths={Path(__file__)};seen=set()
    def visit(mod):
        if id(mod) in seen:return
        seen.add(id(mod));file=Path(getattr(mod,'__file__','/')).resolve()
        if not file.is_relative_to(ROOT/'dembele/pari'):return
        paths.add(file)
        for value in vars(mod).values():
            if isinstance(value,types.ModuleType):visit(value)
        for name in ('CSOURCE','LIBRARY'):
            q=getattr(mod,name,None)
            if q is not None and Path(q).is_file():paths.add(Path(q).resolve())
    for mod in (j,v,coarse):visit(mod)
    return paths

def row_manifest(record,count,bits,weighted,rows,known):
    path=Path(record['path']);assert known[str(path)]==record['sha256'] and source(path)==record
    width=sum((k+7)//8 for bs in v.layout(count,bits,weighted) for k in bs)
    assert path.stat().st_size==rows*width
    hashes=[]
    with path.open('rb') as f:
        for _ in range(rows):
            sha=hashlib.sha256();left=width
            while left:
                raw=f.read(min(left,1<<20));assert len(raw)==min(left,1<<20);sha.update(raw);left-=len(raw)
            hashes.append(sha.hexdigest())
        assert not f.read(1)
    return {'payload':record,'count':count,'bits':bits,'weighted':weighted,'rows':rows,'row_bytes':width,'row_sha256':hashes}

class Engine:
    def __init__(self,config):
        self.config_path=DATA/(config+'.json');self.cfg=json.loads(self.config_path.read_text())
        z=self.cfg;assert z['milestone']=='D132' and z['status']=='pass'
        self.P,self.S,self.column=z['precision_pi'],z['seed_precision_pi'],z['column']
        assert 400<=self.S<self.P<=10552 and self.P%8==self.S%8==0 and 0<=self.column<16
        assert 1<=z['digit_bits']<=200
        self.K=self.P//8;self.path=DATA/z['namespace'];self.store=None;self._inputs=None;self._params={}
        self.masks=[tuple((1<<bit)-1 for bit in bs) for bs in v.layout(self.P,self.K,True)]
    def open(self):
        self.store=j.Store(self.path)
        assert self.store._get('CONFIG.json')=={'config':source(self.config_path),'driver':source(Path(__file__))}
        if self.store._file('CURRENT.json').exists() and not self.store._file('SEALED.json').exists():self.store.recover()
        return self.store
    def inputs(self):
        if self._inputs is None:self._inputs=self.store._get('INPUTS.json')
        return self._inputs
    def reference(self,label,e):
        rr=v.Reader(self.inputs()[label]);values=rr.row(e);rr.close();return values
    def params(self,bits):
        if bits in self._params:return self._params[bits]
        path=DATA/'dyadic_target_transports_d121.json'
        assert source(path)==self.inputs()['transport']
        packet=json.loads(path.read_text());mask=(1<<bits)-1
        def pars(ch):
            assert ch['normalized_error_pi']>=self.P
            return tuple(tuple(int(x)&mask for x in row) for row in ch['normalized_center'][:3])
        self._params[bits]=(packet,pars);return packet,pars
    def masses(self):
        path=DATA/'dyadic_harmonic_certificate_d111.json';assert source(path)==self.inputs()['harmonic']
        return json.loads(path.read_text())['harmonic_basis'][self.column]
    def project(self,values,shift=0):
        return [tuple((x<<shift)&mask for x,mask in zip(row,ms)) for row,ms in zip(values,self.masks)]
    def action(self,e,values,count,rows,bits):
        ring=p.Ring(bits);packet,pars=self.params(bits);total=[b.ZERO]*rows
        for ch in packet['transitions'][e]['children']:
            row=values(ch['target_edge']);assert len(row)==count
            plan=l.Plan(ring,*pars(ch),count,rows);total=ring.padd(total,plan.apply(row));del plan,row
        return total
    def create(self):
        if not self.path.exists() or not (self.path/'CONFIG.json').exists():
            if self.path.exists() and (self.path/'OWNER.json').exists():
                self.store=j.Store(self.path)
                if not self.store._file('WORKSPACE.bin').exists():self.store._reserve('WORKSPACE.bin',j.RESERVE)
            else:self.store=j.Store(self.path,create=True)
            self.store._put('CONFIG.json',{'config':source(self.config_path),'driver':source(Path(__file__))})
        else:self.open()
        st=self.store
        if not st._file('INPUTS.json').exists():
            prior=read('dyadic_weighted_journal_review_d131');known={x['path']:x['sha256'] for x in prior['sources']}
            seed=read(self.cfg['seed']);assert seed['working_precision_pi']==self.S and seed['harmonic_basis_column']==self.column
            assert seed['certificate'].get('original_full_residual_zero') or seed['certificate'].get('original_weighted_fixed_point')
            rec=seed['state_file'] if 'state_file' in seed else seed['checkpoint_files'][0]
            inputs={'seed':row_manifest(rec,self.S,self.S//8,seed.get('weighted_input',False),N,known)}
            refs=[DATA/(self.cfg['seed']+'.json'),DATA/'dyadic_target_transports_d121.json',DATA/'dyadic_harmonic_certificate_d111.json']
            if self.cfg.get('reference'):
                ref=read(self.cfg['reference']);assert ref['working_precision_pi']==self.P and ref['harmonic_basis_column']==self.column
                assert ref['certificate']['original_full_residual_zero']
                inputs['reference']=row_manifest(ref.get('state_file',ref['checkpoint_files'][0]),self.P,self.K,False,N,known)
                refs.append(DATA/(self.cfg['reference']+'.json'))
            cm=read(self.cfg['CM_reference']);assert cm['harmonic_basis_column']==self.column
            inputs['CM_metadata']=source(DATA/(self.cfg['CM_reference']+'.json'));refs.append(Path(inputs['CM_metadata']['path']))
            cmP=cm['working_precision_pi'];inputs['CM_precision_pi']=cmP;inputs['CM_chunks']=cm['moment_chunks']
            for ch in cm['moment_chunks']:
                inputs['CM_'+str(ch['first_chart'])]=row_manifest(ch['file'],2*cmP,cmP//8,False,ch['last_chart']-ch['first_chart']+1,known)
            deps=immutable_dependencies()|set(refs)
            for q in deps:
                if q.name.startswith(('547_','548_')):continue
                assert known[str(q.resolve())]==source(q)['sha256'],str(q)
            inputs['transport']=source(DATA/'dyadic_target_transports_d121.json')
            inputs['harmonic']=source(DATA/'dyadic_harmonic_certificate_d111.json')
            inputs['sources']=[source(q) for q in sorted(deps)]
            st._put('INPUTS.json',inputs)
        width=sum((n+7)//8 for bs in v.layout(self.P,self.K,True) for n in bs)
        st.pool_begin('initial','state.bin',N,width,{'config':source(self.config_path)})
        return {'weighted_state_bytes':N*width,'old_seed_read_as_weighted_representative':True}
    def old_overlap(self,total,e):
        expected=self.reference('seed',e)
        if self.inputs()['seed']['weighted']:
            assert v.encode(total[:self.S],v.layout(self.S,self.S//8,True))==v.encode(expected,v.layout(self.S,self.S//8,True))
        else:assert b.reduce([total[:self.S]],(1<<(self.S//8))-1)==[expected]
    def extend(self,first,last):
        st=self.store;committed=st.pool('initial')['row_sha256'];masses=self.masses();checks=0
        def values(e):
            row=self.reference('seed',e)
            row=decode(v.encode(row,v.layout(self.S,self.S//8,True)),self.S,self.S//8,True)
            row[0]=(masses[e]&((1<<self.K)-1),)+(0,)*7;return row
        for e in range(first,last+1):
            if committed[e] is not None:st.pool_read('initial',e);continue
            total=self.action(e,values,self.S,self.P,self.K)
            assert total[0]==(masses[e]&((1<<self.K)-1),)+(0,)*7
            self.old_overlap(total,e)
            st.pool_row('initial',e,v.encode(total,v.layout(self.P,self.K,True)));checks+=self.S*8
        return {'first':first,'last':last,'old_uniform_scalar_overlaps':checks,'original_child_actions':2*(last-first+1)}
    def init_finish(self):
        st=self.store;st.pool_finish('initial');cur=st.finish_initialization({'seed_precision_pi':self.S})
        return {'generation':cur['tag'],'state_sha256':cur['state']['sha256']}
    def ctx(self,step):return self.store._get(f'low_{step:03d}.json')
    def low_begin(self,step):
        st=self.store;cur=st.current();seed=step==0
        assert cur['tag']==('initial' if seed else f'ready{step-1:03d}') and cur['phase']=='ready'
        u=0 if seed else self.S+33*(step-1);count=self.P if seed else max(33,self.P-u)
        shift=u//8;bits=self.K-shift
        assert seed or count>33
        d={'step':step,'seed':seed,'base':cur,'u':u,'shift':shift,'bits':bits,'count':count,
           'digits':list(range(min(bits,self.cfg['digit_bits']),bits,self.cfg['digit_bits']))+[bits]}
        name=f'low_{step:03d}.json'
        with st.guard():
            if st._file(name).exists():assert st._get(name)==d
            else:st._put(name,d)
        st.pool_begin(f'rhs{step:03d}',f'rhs{step:03d}.bin',N,R*8*((bits+7)//8),{'base_tag':cur['tag']})
        return {'bits':bits,'digits':d['digits'],'base_tag':cur['tag']}
    def rhs(self,step,first,last):
        st=self.store;d=self.ctx(step);label=f'rhs{step:03d}';committed=st.pool(label)['row_sha256']
        def values(e):
            row=decode(st.read_row('state' if d['seed'] else 'aux',e,d['base']['tag']),d['count'],d['bits'],d['seed'])
            row[1:33]=[b.ZERO]*32;return row
        for e in range(first,last+1):
            if committed[e] is not None:st.pool_read(label,e);continue
            total=self.action(e,values,d['count'],33,d['bits'])
            if not d['seed']:assert total[0]==b.ZERO
            st.pool_row(label,e,b.pack([[x] for x in total[1:]],d['bits']))
        return {'first':first,'last':last,'original_child_actions':2*(last-first+1),'bits':d['bits']}
    def original(self,values,bits):
        packet,pars=self.params(bits);groups={};alg=b.Algebra(bits);out=list(values)
        for e,edge in enumerate(packet['transitions']):
            for ch in edge['children']:groups.setdefault(pars(ch),[]).append((e,ch['target_edge']))
        for par,dests in groups.items():
            block=b.coefficients(par,R,alg)
            for e,ch in dests:out[e]=alg.sub(out[e],alg.mul(block,values[ch]))
            del block
        return out
    def low_values(self,label,bits):
        self.store.pool(label,True)
        return [low_decode(self.store.pool_read(label,e),bits) for e in range(N)]
    def write_low(self,label,values,bits,authority):
        st=self.store;st.pool_begin(label,label+'.bin',N,R*8*((bits+7)//8),authority)
        for e,row in enumerate(values):st.pool_row(label,e,low_pack(row,bits))
        return st.pool_finish(label)
    def low_residual(self,step,digit):
        st=self.store;d=self.ctx(step);new=d['digits'][digit];old=d['digits'][digit-1] if digit else 0
        st.pool_finish(f'rhs{step:03d}')
        rhs=[b.reduce(edge,(1<<new)-1) for edge in self.low_values(f'rhs{step:03d}',d['bits'])]
        if old:
            valid=st._get(f'valid{step:03d}_{digit-1:02d}.json');assert valid['bits']==old
            prior=self.low_values(f'answer{step:03d}_{digit-1:02d}',old)
            applied=self.original(prior,new);alg=b.Algebra(new)
            rhs=[alg.sub(x,y) for x,y in zip(rhs,applied)]
            assert all(v&((1<<old)-1)==0 for edge in rhs for row in edge for x in row for v in x)
            rhs=[[[tuple(v>>old for v in x) for x in row] for row in edge] for edge in rhs]
        info=self.write_low(f'quotient{step:03d}_{digit:02d}',rhs,new-old,{'old_bits':old,'new_bits':new})
        return {'old_bits':old,'new_bits':new,'exact_divisions':N*R*8 if old else 0,'quotient_sha256':info['sha256']}
    def low_solve(self,step,digit):
        st=self.store;d=self.ctx(step);new=d['digits'][digit];old=d['digits'][digit-1] if digit else 0
        rhs=self.low_values(f'quotient{step:03d}_{digit:02d}',new-old)
        factor=c.FactorReader(new-old);delta=factor.solve(rhs,b.Algebra(new-old));factor.close();assert factor.decoded_blocks==1226
        if old:
            prior=self.low_values(f'answer{step:03d}_{digit-1:02d}',old)
            answer=[[[tuple(x+(y<<old) for x,y in zip(a,z)) for a,z in zip(row,dr)] for row,dr in zip(edge,de)] for edge,de in zip(prior,delta)]
        else:answer=delta
        info=self.write_low(f'answer{step:03d}_{digit:02d}',answer,new,{'old_bits':old,'new_bits':new})
        return {'bits':new,'factor_bits':new-old,'factor_blocks':1226,'answer_sha256':info['sha256']}
    def low_verify(self,step,digit):
        st=self.store;d=self.ctx(step);bits=d['digits'][digit]
        label=f'answer{step:03d}_{digit:02d}';answer=self.low_values(label,bits)
        rhs=[b.reduce(edge,(1<<bits)-1) for edge in self.low_values(f'rhs{step:03d}',d['bits'])]
        assert self.original(answer,bits)==rhs
        info=st.pool(label,True);valid={'bits':bits,'answer_sha256':info['sha256'],'all_original_low_equations':N*R*8}
        with st.guard():st._put(f'valid{step:03d}_{digit:02d}.json',valid)
        st.pool_retire(f'quotient{step:03d}_{digit:02d}')
        if digit:st.pool_retire(f'answer{step:03d}_{digit-1:02d}')
        return valid
    def prepare_begin(self,step):
        st=self.store;d=self.ctx(step);last=len(d['digits'])-1
        valid=st._get(f'valid{step:03d}_{last:02d}.json');assert valid['bits']==d['bits']
        with st.guard():
            initial=st._get('pool_initial.json');initial['historical_after_state_update']=True;st._put('pool_initial.json',initial)
        if st._file('TXN.json').exists():
            tx=st._get('TXN.json');assert tx['kind']=='prepare' and tx['target']==f'prepared{step:03d}'
        else:st.begin_prepare(f'prepared{step:03d}',{'step':step,'low_answer':valid,'u':d['u']})
        return {'step':step,'low_answer_verified':True}
    def prepare_rows(self,step,first,last):
        st=self.store;d=self.ctx(step);digit=len(d['digits'])-1;label=f'answer{step:03d}_{digit:02d}'
        for e in range(first,last+1):
            st.recover();tx=st._get('TXN.json');assert tx['kind']=='prepare' and tx['target']==f'prepared{step:03d}'
            if e<tx['next_row']:continue
            assert e==tx['next_row'];base=tx['base']
            answer=decode(st.pool_read(label,e),R,d['bits']);state=decode(st._readrow(base['state'],e),self.P,self.K,True)
            oldaux=st._readrow(base['aux'],e)
            if d['seed']:
                state[1:33]=answer;aux=oldaux
            else:
                correction=decode(oldaux,d['count'],d['bits']);assert correction[:33]==[b.ZERO]*33
                correction[1:33]=answer
                shifted=[tuple(x<<d['shift'] for x in row) for row in correction]
                assert l.value([shifted],self.P)>=d['u']
                for k,row in enumerate(shifted):state[k]=tuple((x+y)&m for x,y,m in zip(state[k],row,self.masks[k]))
                aux=b.pack([correction],d['bits'])
            st.prepare_row(e,v.encode(state,v.layout(self.P,self.K,True)),aux)
        return {'first':first,'last':last,'prepared_rows':last-first+1}
    def prepare_finish(self,step):
        st=self.store;d=self.ctx(step)
        cur=st.finish_prepare() if st._file('TXN.json').exists() else st.current()
        assert cur['tag']==f'prepared{step:03d}' and cur['phase']=='prepared'
        st.pool_retire(f'rhs{step:03d}');st.pool_retire(f"answer{step:03d}_{len(d['digits'])-1:02d}")
        return {'tag':cur['tag'],'state_sha256':cur['state']['sha256'],'correction_sha256':cur['aux']['sha256']}
    def sweep_begin(self,step):
        st=self.store;d=self.ctx(step);u=self.S if d['seed'] else min(self.P,d['u']+33)
        count=max(33,self.P-u);bits=self.K-u//8;assert bits>0
        if st._file('TXN.json').exists():
            tx=st._get('TXN.json');assert tx['kind']=='sweep' and tx['target']==f'ready{step:03d}'
        else:st.begin_sweep(f'ready{step:03d}',count*8*((bits+7)//8),{'u':u,'count':count,'bits':bits})
        return {'after_pi':u,'count':count,'bits':bits}
    def operator(self,step,first,last):
        st=self.store;d=self.ctx(step);tx=st._get('TXN.json');assert tx['kind']=='sweep' and tx['target']==f'ready{step:03d}'
        after=tx['authority'];count=after['count'];tag=tx['base']['tag']
        def values(e):return decode(st.read_row('state' if d['seed'] else 'aux',e,tag,operator=True),d['count'],d['bits'],d['seed'])
        hashes=[]
        for e in range(first,last+1):
            if tx['row_hashes'][e] is not None:
                info={'name':tx['name'],'row_bytes':tx['width'],'rows':N,'bytes':N*tx['width'],'row_sha256':tx['row_hashes']}
                raw=st._readrow(info,e)
            else:
                total=self.action(e,values,d['count'],count,d['bits'])
                if d['seed']:
                    own=values(e);mask=(1<<self.K)-1
                    total=[tuple((x-y)&mask for x,y in zip(a,z)) for a,z in zip(total,own)]
                    assert total[:33]==[b.ZERO]*33;projected=self.project(total)
                else:
                    assert total[:33]==values(e)[:33];total[:33]=[b.ZERO]*33
                    projected=self.project(total,d['shift'])
                assert l.value([projected],self.P)>=after['u']
                shift=after['u']//8;assert all(x&((1<<shift)-1)==0 for row in projected for x in row)
                raw=b.pack([[tuple(x>>shift for x in row) for row in projected]],after['bits'])
                st.sweep_row(e,raw)
            hashes.append(hashlib.sha256(raw).hexdigest())
        return {'first':first,'last':last,'after_pi':after['u'],'count':count,'row_sha256':hashes}
    def sweep_finish(self,step):
        st=self.store;cur=st.finish_sweep() if st._file('TXN.json').exists() else st.current()
        assert cur['tag']==f'ready{step:03d}' and cur['phase']=='ready'
        return {'tag':cur['tag'],'u':cur['authority']['u'],'count':cur['authority']['count'],'residual_sha256':cur['aux']['sha256']}
    def verify_begin(self):
        st=self.store;cur=st.current();assert cur['authority']['count']==33 and cur['authority']['u']+33>=self.P
        for e in range(N):assert not any(st.read_row('aux',e,cur['tag']))
        st.pool_begin('verification','verification.bin',N,32,{'tag':cur['tag'],'state_sha256':cur['state']['sha256']})
        return {'weighted_residual_is_zero':True,'tag':cur['tag']}
    def verify(self,first,last):
        st=self.store;cur=st.current();tag=cur['tag'];masses=self.masses()
        def values(e):return decode(st.read_row('state',e,tag),self.P,self.K,True)
        for e in range(first,last+1):
            if st.pool('verification')['row_sha256'][e] is not None:st.pool_read('verification',e);continue
            total=self.action(e,values,self.P,self.P,self.K)
            assert v.encode(total,v.layout(self.P,self.K,True))==st.read_row('state',e,tag)
            assert total[0]==(masses[e]&((1<<self.K)-1),)+(0,)*7
            self.old_overlap(total,e)
            if 'reference' in self.inputs():assert total==self.reference('reference',e)
            st.pool_row('verification',e,hashlib.sha256(b.pack([total],self.K)).digest())
        return {'first':first,'last':last,'weighted_equation_scalars':(last-first+1)*self.P*8,'masses':last-first+1}
    def cm_begin(self):
        st=self.store;info=st.pool_finish('verification');cur=st.current()
        with st.guard():st._put('VERIFIED.json',{'tag':cur['tag'],'state':cur['state'],'verification':info,'all_QT_w_equals_w':True,'masses':N})
        st.pool_begin('CM','CM.bin',17,2*self.P*8*((self.K+7)//8),{'tag':cur['tag']})
        return {'all_weighted_equations_checked':N*self.P*8,'CM_payload_bytes':17*2*self.P*8*((self.K+7)//8)}
    def cm(self,first,last):
        st=self.store;verified=st._get('VERIFIED.json');cur=st.current();assert verified['state']==cur['state']
        ring=p.Ring(self.K);packet,pars=self.params(self.K);charts=[x for x in packet['CM_charts'] if x['chart']=='A'];oldP=self.inputs()['CM_precision_pi']
        for ci in range(first,last+1):
            if st.pool('CM')['row_sha256'][ci] is not None:st.pool_read('CM',ci);continue
            chart=charts[ci];A,B,C=pars(chart);total=[b.ZERO]*(2*self.P)
            for ch in packet['transitions'][chart['target_edge']]['children']:
                a,bb,cc=pars(ch);den=ring.add(b.ONE,ring.mul(C,bb));inv=b.ONE;two=(2,)+(0,)*7
                for _ in range(self.P.bit_length()):inv=ring.mul(inv,ring.add(two,ring.neg(ring.mul(den,inv))))
                assert ring.mul(den,inv)==b.ONE
                par=(ring.mul(ring.add(ring.mul(A,a),ring.mul(B,cc)),inv),ring.mul(ring.add(ring.mul(A,bb),B),inv),ring.mul(ring.add(cc,ring.mul(C,a)),inv))
                row=decode(st.read_row('state',ch['target_edge'],cur['tag']),self.P,self.K,True)
                plan=l.Plan(ring,*par,self.P,2*self.P);total=ring.padd(total,plan.apply(row));del plan,row
            assert total[0]==(chart['zeroth_moments'][self.column]&ring.mask,)+(0,)*7
            ch=next(x for x in self.inputs()['CM_chunks'] if x['first_chart']<=ci<=x['last_chart'])
            old=self.reference('CM_'+str(ch['first_chart']),ci-ch['first_chart']);cut=2*min(self.P,oldP);mask=(1<<(min(self.P,oldP)//8))-1
            assert b.reduce([total[:cut]],mask)==b.reduce([old[:cut]],mask)
            st.pool_row('CM',ci,b.pack([total],self.K))
        return {'first':first,'last':last,'CM_scalars':(last-first+1)*2*self.P*8,'old_overlap_precision_pi':min(self.P,oldP)}
    def coarse(self,chart,order):
        st=self.store;st.pool_finish('CM');moments=decode(st.pool_read('CM',chart),2*self.P,self.K)
        ring=coarse.Ring(2*self.P+64);pi=ring.add(ring.scale(ring.mul(coarse.BETA,coarse.BETA),-1),ring.scale(coarse.ONE,-2))
        q=ring.add(tuple(coarse.MP[1:]),ring.scale(coarse.BETA,-1));assert ring.mul(q,coarse.BETA)==pi
        powers=ring.powers(pi,7);answer=coarse.ZERO;power=coarse.ONE;n=2*order+2
        for k,row in enumerate(moments):
            embedded=coarse.ZERO
            for value,basis in zip(row,powers):embedded=ring.add(embedded,ring.scale(basis,value))
            answer=ring.add(answer,ring.mul(ring.scale(power,coarse.coefficient(n,k)),embedded));power=ring.mul(power,q)
        gain=16*min(k+(comb(n,k)&-comb(n,k)).bit_length()-1 for k in range(1,n+1));error=2*self.P+gain
        old=json.loads(Path(self.inputs()['CM_metadata']['path']).read_text())
        assert source(self.inputs()['CM_metadata']['path'])==self.inputs()['CM_metadata']
        prior=tuple(old['CM_values'][chart]['coarse_coefficients_beta'][order])
        assert ring.value(ring.add(answer,ring.scale(prior,-1)))>=min(error,old['coarse_error_beta'][order])
        return {'chart':chart,'order':order,'coarse_value_beta':list(answer),'error_beta':error,'old_overlap_checked':True}
    def seal(self):
        st=self.store
        if st._file('SEALED.json').exists():st.pool('CM',True)
        else:st.pool_finish('CM')
        verified=st._get('VERIFIED.json');assert verified['all_QT_w_equals_w']
        for ci in range(17):
            for order in range(4):assert st._file(f'done_coarse_c{ci:02d}_o{order}.json').exists()
        if st._file('SEALED.json').exists():
            cur=st.current();assert st._get('SEALED.json')['current_sha256']==j.digest(j.canonical(cur))
            for kind in ('state','aux'):
                x=cur[kind];assert st._info(x['name'],x['row_bytes'],x['rows'],x['row_sha256'])==x
        else:cur=st.seal()
        return {'precision_pi':self.P,'new_mathematical_precision':not bool(self.cfg.get('reference')),
                'weighted_state':cur['state'],'CM':st.pool('CM',True),'residual':cur['aux']}

def dispatch(eng,a):
    if a.phase=='create':return eng.create()
    eng.open();st=eng.store
    method=getattr(eng,a.phase.replace('-','_'))
    if a.phase in ('extend','verify','cm'):return method(a.first,a.last)
    if a.phase in ('rhs','prepare-rows','operator'):return method(a.step,a.first,a.last)
    if a.phase in ('low-residual','low-solve','low-verify'):return method(a.step,a.digit)
    if a.phase in ('low-begin','prepare-begin','prepare-finish','sweep-begin','sweep-finish'):return method(a.step)
    if a.phase=='coarse':return method(a.chart,a.order)
    return method()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--config',required=True);ap.add_argument('--phase',required=True);ap.add_argument('--key',required=True);ap.add_argument('--output',required=True)
    for name in ('step','digit','first','last','chart','order'):ap.add_argument('--'+name,type=int)
    ap.add_argument('--fault');ap.add_argument('--fault-row',type=int)
    a=ap.parse_args();assert all(__import__('re').fullmatch(r'[A-Za-z0-9_]+',x) for x in (a.config,a.key,a.output))
    eng=Engine(a.config);name='done_'+a.key+'.json';out=DATA/(a.output+'.json')
    request={k:v for k,v in vars(a).items() if k not in ('output','fault','fault_row')}
    if out.exists():
        packet=json.loads(out.read_text());assert packet['status']=='pass' and packet['request']==request
        assert packet['driver']==source(Path(__file__)) and packet['config']==source(eng.config_path)
        print('PHASE_METADATA|'+json.dumps(source(out)),flush=True);print('PASS|548_DYADIC_RESUMABLE_STAGED_DRIVER',flush=True);return
    if eng.path.exists() and (eng.path/'CONFIG.json').exists():
        eng.open()
        if eng.store._file(name).exists():
            packet=eng.store._get(name);assert packet['request']==request
            assert not out.exists() or json.loads(out.read_text())==packet
            if not out.exists():
                tmp=out.with_suffix('.json.tmp')
                with tmp.open('w') as f:f.write(json.dumps(packet,indent=2)+'\n');f.flush();os.fsync(f.fileno())
                os.replace(tmp,out)
            print('PHASE_METADATA|'+json.dumps(source(out)),flush=True);print('PASS|548_DYADIC_RESUMABLE_STAGED_DRIVER',flush=True);return
    tick=time.monotonic();original_crash=j.Store._crash
    def crash(st,point):
        if a.fault==point:
            if a.fault_row is None:os._exit(73)
            if st._file('TXN.json').exists():
                tx=st._get('TXN.json')
                if tx.get('next_row')==a.fault_row:os._exit(73)
        original_crash(st,point)
    j.Store._crash=crash
    cert=dispatch(eng,a);st=eng.store
    packet={'status':'pass','milestone':'D132','request':request,'config':source(eng.config_path),'driver':source(Path(__file__)),
            'certificates':cert,'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':peak(),
            'maximum_observed_store_bytes':st.peak,'historical_payload_hashes_are_not_retained_source_claims':True}
    packet.update(working_precision_pi=eng.P,harmonic_basis_column=eng.column)
    if a.phase=='seal':
        packet.update(certificate={'original_weighted_fixed_point':True,'all_fixed_masses':True},weighted_input=True,
                      state_file={'path':str(st.path/cert['weighted_state']['name']),'sha256':cert['weighted_state']['sha256']})
    assert packet['peak_rss_bytes']<=2*(1<<30),'per-job measured RSS admission exceeded'
    assert len(j.canonical(packet))<=(65536 if a.phase=='seal' else 8192),'phase record exceeds inventory allowance'
    # Sealing freezes the store; its final completion record is external.
    if a.phase!='seal':
        with st.guard():st._put(name,packet)
    if a.fault=='job_committed':os._exit(73)
    if out.exists():assert json.loads(out.read_text())==packet
    else:
        tmp=out.with_suffix('.json.tmp')
        with tmp.open('w') as f:f.write(json.dumps(packet,indent=2)+'\n');f.flush();os.fsync(f.fileno())
        os.replace(tmp,out)
    print('PHASE_METADATA|'+json.dumps(source(out)),flush=True)
    print('D132_PHASE|'+json.dumps({'key':a.key,'seconds':packet['wall_seconds'],'peak_rss_bytes':packet['peak_rss_bytes'],'store_bytes':st.peak}),flush=True)
    print('PASS|548_DYADIC_RESUMABLE_STAGED_DRIVER',flush=True)

if __name__=='__main__':main()
