"""D132 resumable staged row store: durable redo, epoch barriers, row hashes.

Only a new owned namespace can mutate. This module implements storage, not
the mathematical correction solver. A caller must certify proposed rows.
Process-interruption recovery is tested separately; power-loss durability
is not claimed from those tests. All allocations count full logical sizes.
"""
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'dembele/data/computed'
CAP=2*(1<<30)
RESERVE=64*(1<<20)
CODE_SHA=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def digest(raw):return hashlib.sha256(raw).hexdigest()
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
def envelope(value):return {'value':value,'sha256':digest(canonical(value))}


class Store:
    def __init__(self,path,create=False,fault=None):
        self.path=Path(path).resolve();self.fault=fault;self.peak=0
        assert self.path.parent==DATA and re.fullmatch(r'dyadic_rowjournal_[A-Za-z0-9_]+_d132',self.path.name)
        if create:
            owner={'namespace':self.path.name,'storage_source_sha256':CODE_SHA,
                   'cap_bytes':CAP,'payloads_prospectively_transient_until_seal':True}
            if self.path.exists():
                assert self.path.is_dir() and not self.path.is_symlink()
                assert {x.name for x in self.path.iterdir()}<= {'OWNER.json','OWNER.json.tmp','WORKSPACE.bin'}
                if self._file('OWNER.json').exists():assert self._get('OWNER.json')==owner
                elif self._file('OWNER.json.tmp').exists():assert self._get('OWNER.json.tmp')==owner
            else:self.path.mkdir()
            self._put('OWNER.json',owner)
            if self._file('WORKSPACE.bin').exists() and self._file('WORKSPACE.bin').stat().st_size!=RESERVE:self._remove('WORKSPACE.bin')
            if not self._file('WORKSPACE.bin').exists():self._reserve('WORKSPACE.bin',RESERVE)
        assert self.path.is_dir() and not self.path.is_symlink()
        owner=self._get('OWNER.json')
        assert owner['namespace']==self.path.name and owner['storage_source_sha256']==CODE_SHA and owner['cap_bytes']==CAP

    def _file(self,name):
        assert re.fullmatch(r'[A-Za-z0-9_.-]+',name) and name not in ('.','..')
        path=self.path/name;assert not path.is_symlink();return path

    def _syncdir(self):
        fd=os.open(self.path,os.O_RDONLY)
        try:os.fsync(fd)
        finally:os.close(fd)

    def occupied(self):
        paths=list(self.path.iterdir());assert all(p.is_file() and not p.is_symlink() for p in paths)
        size=sum(p.stat().st_size for p in paths);assert size<=CAP,'scratch cap exceeded'
        self.peak=max(self.peak,size);return size

    def _reserve(self,name,size):
        assert isinstance(size,int) and size>=0
        p=self._file(name);assert not p.exists()
        assert self.occupied()+size<=CAP,'scratch reservation exceeds cap'
        with p.open('xb') as f:f.truncate(size);f.flush();os.fsync(f.fileno())
        self.occupied()

    def _put(self,name,value):
        raw=canonical(envelope(value));tmp=self._file(name+'.tmp')
        if tmp.exists():tmp.unlink() # Uncommitted metadata only, under lock.
        assert self.occupied()+len(raw)<=CAP,'scratch reservation exceeds cap'
        with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        self.occupied();os.replace(tmp,self._file(name));self._syncdir()

    def _get(self,name):
        packet=json.loads(self._file(name).read_text())
        assert set(packet)=={'value','sha256'} and digest(canonical(packet['value']))==packet['sha256'],'metadata digest mismatch'
        return packet['value']

    def _crash(self,point):
        if self.fault==point:os._exit(73)

    @contextmanager
    def guard(self,write=True):
        with self._file('.lock').open('a+b') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            if write:assert not self._file('SEALED.json').exists(),'sealed store is immutable'
            self.occupied();yield;self.occupied()

    def _remove(self,name):
        p=self._file(name)
        if p.exists():p.unlink();self._syncdir()

    def _info(self,name,width,rows,expected=None):
        path=self._file(name);assert path.stat().st_size==width*rows
        full=hashlib.sha256();hashes=[]
        with path.open('rb') as f:
            for e in range(rows):
                sha=hashlib.sha256();left=width
                while left:
                    raw=f.read(min(left,1<<20));assert len(raw)==min(left,1<<20)
                    sha.update(raw);full.update(raw);left-=len(raw)
                hashes.append(sha.hexdigest())
                if expected is not None:assert hashes[-1]==expected[e],'row digest mismatch'
            assert not f.read(1)
        return {'name':name,'row_bytes':width,'rows':rows,'bytes':width*rows,
                'row_sha256':hashes,'sha256':full.hexdigest()}

    def _readrow(self,info,e):
        assert 0<=e<info['rows'] and self._file(info['name']).stat().st_size==info['bytes']
        with self._file(info['name']).open('rb') as f:f.seek(e*info['row_bytes']);raw=f.read(info['row_bytes'])
        assert len(raw)==info['row_bytes'] and digest(raw)==info['row_sha256'][e],'row digest mismatch'
        return raw

    def _writeat(self,name,offset,raw,partial=None):
        assert offset>=0 and offset+len(raw)<=self._file(name).stat().st_size
        with self._file(name).open('r+b') as f:
            f.seek(offset)
            if partial and self.fault==partial:
                f.write(raw[:max(1,len(raw)//2)]);f.flush();os.fsync(f.fileno());self._crash(partial)
            assert f.write(raw)==len(raw);f.flush();os.fsync(f.fileno())

    def initialize(self,rows,state_width,aux_width,state_rows,aux_rows,authority):
        with self.guard():
            assert not self._file('CURRENT.json').exists() and not self._file('TXN.json').exists()
            for name,width,iterator in (('state.bin',state_width,state_rows),('aux_initial.bin',aux_width,aux_rows)):
                if self._file(name).exists():self._remove(name) # Restart uncommitted initialization.
                self._reserve(name,rows*width)
                with self._file(name).open('r+b') as f:
                    count=0
                    for raw in iterator:
                        assert len(raw)==width and count<rows;assert f.write(raw)==width;count+=1
                    assert count==rows;f.flush();os.fsync(f.fileno())
                if name=='state.bin':self._crash('initial_state_written')
            state=self._info('state.bin',state_width,rows);aux=self._info('aux_initial.bin',aux_width,rows)
            self._put('CURRENT.json',{'tag':'initial','phase':'ready','epoch':0,'state':state,'aux':aux,'authority':authority})

    def current(self):
        with self.guard(False):
            assert not self._file('TXN.json').exists(),'generation is incomplete'
            return self._get('CURRENT.json')

    def read_row(self,kind,e,tag,operator=False):
        with self.guard(False):
            c=self._get('CURRENT.json');assert c['tag']==tag,'stale generation'
            if self._file('TXN.json').exists():
                t=self._get('TXN.json')
                assert operator and t['kind']=='sweep' and t['base']==c,'mixed generation is not readable'
            assert kind in ('state','aux')
            return self._readrow(c[kind],e)

    def begin_prepare(self,tag,authority):
        assert re.fullmatch(r'[A-Za-z0-9_]+',tag)
        with self.guard():
            self._recover();assert not self._file('TXN.json').exists()
            c=self._get('CURRENT.json');assert c['phase']=='ready' and tag!=c['tag']
            for k in ('state','aux'):assert self._info(c[k]['name'],c[k]['row_bytes'],c[k]['rows'],c[k]['row_sha256'])==c[k]
            self._put(f"history_{c['epoch']:04d}.json",c)
            self._put('TXN.json',{'kind':'prepare','base':c,'target':tag,'authority':authority,
                                  'next_row':0,'state_hashes':[],'aux_hashes':[]})
            self._crash('prepare_intent')

    def _wal_cleanup(self):
        existed=self._file('WAL.json').exists()
        self._remove('WAL.json')
        if existed:self._crash('wal_unlinked')
        for name in ('wal_before_state.bin','wal_after_state.bin','wal_before_aux.bin','wal_after_aux.bin'):self._remove(name)

    def prepare_row(self,e,new_state,new_aux):
        with self.guard():
            self._recover();t=self._get('TXN.json');assert t['kind']=='prepare' and t['next_row']==e
            c=t['base'];assert len(new_state)==c['state']['row_bytes'] and len(new_aux)==c['aux']['row_bytes']
            old_state=self._readrow(c['state'],e);old_aux=self._readrow(c['aux'],e)
            blobs={'before_state':old_state,'after_state':new_state,'before_aux':old_aux,'after_aux':new_aux}
            records={}
            for key,raw in blobs.items():
                name='wal_'+key+'.bin';self._reserve(name,len(raw));self._writeat(name,0,raw)
                records[key]={'name':name,'bytes':len(raw),'sha256':digest(raw)}
            self._crash('wal_blobs_uncommitted')
            self._put('WAL.json',{'target':t['target'],'base_tag':c['tag'],'row':e,'blobs':records})
            self._crash('wal_committed')
            self._writeat(c['state']['name'],e*c['state']['row_bytes'],new_state,'state_half')
            self._crash('state_written')
            self._writeat(c['aux']['name'],e*c['aux']['row_bytes'],new_aux,'aux_half')
            self._crash('aux_written')
            t['next_row']+=1;t['state_hashes'].append(digest(new_state));t['aux_hashes'].append(digest(new_aux))
            self._put('TXN.json',t);self._crash('progress_committed');self._wal_cleanup()

    def finish_prepare(self):
        with self.guard():
            self._recover();t=self._get('TXN.json');assert t['kind']=='prepare'
            c=t['base'];assert t['next_row']==c['state']['rows']==c['aux']['rows']
            result={'tag':t['target'],'phase':'prepared','epoch':c['epoch']+1,'authority':t['authority']}
            for k in ('state','aux'):
                result[k]=self._info(c[k]['name'],c[k]['row_bytes'],c[k]['rows'],t[k+'_hashes'])
            self._put('CURRENT.json',result);self._crash('prepare_generation_committed');self._remove('TXN.json')
            return result

    def begin_sweep(self,tag,width,authority):
        assert re.fullmatch(r'[A-Za-z0-9_]+',tag) and width>0
        with self.guard():
            self._recover();assert not self._file('TXN.json').exists()
            c=self._get('CURRENT.json');assert c['phase']=='prepared' and tag!=c['tag']
            self._put(f"history_{c['epoch']:04d}.json",c)
            name='aux_'+tag+'.bin';assert not self._file(name).exists()
            self._put('TXN.json',{'kind':'sweep','base':c,'target':tag,'authority':authority,'name':name,
                                  'width':width,'row_hashes':[None]*c['state']['rows']})
            self._crash('sweep_intent')
            self._reserve(name,width*c['state']['rows'])

    def sweep_row(self,e,raw):
        with self.guard():
            self._recover();t=self._get('TXN.json');assert t['kind']=='sweep'
            assert len(raw)==t['width'] and 0<=e<len(t['row_hashes'])
            if t['row_hashes'][e] is not None:
                assert digest(raw)==t['row_hashes'][e]
                info={'name':t['name'],'row_bytes':t['width'],'rows':len(t['row_hashes']),
                      'bytes':t['width']*len(t['row_hashes']),'row_sha256':t['row_hashes']}
                assert self._readrow(info,e)==raw;return
            self._writeat(t['name'],e*t['width'],raw,'sweep_half');self._crash('sweep_row_written')
            t['row_hashes'][e]=digest(raw);self._put('TXN.json',t);self._crash('sweep_progress_committed')

    def finish_sweep(self):
        with self.guard():
            self._recover();t=self._get('TXN.json');assert t['kind']=='sweep' and all(t['row_hashes'])
            c=t['base'];aux=self._info(t['name'],t['width'],len(t['row_hashes']),t['row_hashes'])
            state=c['state'];assert self._info(state['name'],state['row_bytes'],state['rows'],state['row_sha256'])==state
            assert self._info(c['aux']['name'],c['aux']['row_bytes'],c['aux']['rows'],c['aux']['row_sha256'])==c['aux']
            result={'tag':t['target'],'phase':'ready','epoch':c['epoch']+1,'authority':t['authority'],'state':state,'aux':aux}
            self._put('RETIRE.json',{'after_tag':t['target'],'name':c['aux']['name'],'old_info':c['aux']})
            self._crash('retirement_intent')
            self._put('CURRENT.json',result);self._crash('sweep_generation_committed')
            self._remove('TXN.json');self._crash('sweep_intent_removed');self._retire()
            return result

    def _retire(self):
        if not self._file('RETIRE.json').exists():return
        r=self._get('RETIRE.json');c=self._get('CURRENT.json')
        if c['tag']!=r['after_tag']:return
        assert r['name'] not in (c['state']['name'],c['aux']['name'])
        if self._file(r['name']).exists():
            i=r['old_info'];assert self._info(i['name'],i['row_bytes'],i['rows'],i['row_sha256'])==i
        self._remove(r['name']);self._crash('retired_file_unlinked')
        self._put(f"retired_{c['epoch']:04d}.json",r);self._remove('RETIRE.json')

    def _recover(self):
        for tmp in self.path.glob('*.tmp'):self._remove(tmp.name)
        if self._file('TXN.json').exists():
            t=self._get('TXN.json');c=self._get('CURRENT.json')
            if c['tag']==t['target']:
                assert c['phase']==('prepared' if t['kind']=='prepare' else 'ready')
                self._remove('TXN.json');self._wal_cleanup();self._retire();return
            assert c==t['base'],'transaction base changed'
            if self._file('WAL.json').exists():
                v=self._get('WAL.json');e=v['row'];assert t['kind']=='prepare'
                assert v['target']==t['target'] and v['base_tag']==c['tag'] and t['next_row'] in (e,e+1)
                blobs={}
                for key,record in v['blobs'].items():
                    raw=self._file(record['name']).read_bytes()
                    assert len(raw)==record['bytes'] and digest(raw)==record['sha256'],'WAL digest mismatch'
                    blobs[key]=raw
                assert set(blobs)=={'before_state','after_state','before_aux','after_aux'}
                for kind in ('state','aux'):
                    assert digest(blobs['before_'+kind])==c[kind]['row_sha256'][e]
                    self._writeat(c[kind]['name'],e*c[kind]['row_bytes'],blobs['after_'+kind])
                if t['next_row']==e:
                    t['next_row']+=1;t['state_hashes'].append(digest(blobs['after_state']));t['aux_hashes'].append(digest(blobs['after_aux']))
                    self._put('TXN.json',t)
                else:
                    assert t['state_hashes'][e]==digest(blobs['after_state']) and t['aux_hashes'][e]==digest(blobs['after_aux'])
                self._wal_cleanup()
            else:
                self._wal_cleanup() # Uncommitted WAL blobs; no data write preceded WAL commit.
            if t['kind']=='sweep':
                if not self._file(t['name']).exists():self._reserve(t['name'],t['width']*len(t['row_hashes']))
                if self._file(t['name']).stat().st_size != t['width']*len(t['row_hashes']):
                    assert not any(t['row_hashes'])
                    self._remove(t['name']);self._reserve(t['name'],t['width']*len(t['row_hashes']))
        else:self._wal_cleanup()
        self._retire()

    def recover(self):
        with self.guard():self._recover()

    def seal(self):
        with self.guard():
            self._recover();assert not self._file('TXN.json').exists() and not self._file('RETIRE.json').exists()
            c=self._get('CURRENT.json')
            for k in ('state','aux'):assert self._info(c[k]['name'],c[k]['row_bytes'],c[k]['rows'],c[k]['row_sha256'])==c[k]
            peak=self.peak;self._remove('WORKSPACE.bin')
            self._put('SEALED.json',{'current_sha256':digest(canonical(c)),'all_remaining_files_frozen':True,
                                     'maximum_observed_logical_bytes_in_this_process':peak,
                                     'history_payload_hashes_are_not_retained_source_hashes':True})
            return c

    def pool_begin(self,label,name,rows,width,authority):
        """Reserve a row pool before computation; retries preserve committed rows."""
        assert re.fullmatch(r'[A-Za-z0-9_]+',label) and rows>0 and width>0
        with self.guard():
            meta='pool_'+label+'.json'
            spec={'name':name,'rows':rows,'row_bytes':width,'bytes':rows*width,'authority':authority}
            if self._file(meta).exists():
                d=self._get(meta);assert all(d[k]==v for k,v in spec.items()) and not d.get('retired')
            else:
                d=spec|{'row_sha256':[None]*rows,'complete':False};self._put(meta,d)
                self._crash('pool_intent')
            if self._file(name).exists() and self._file(name).stat().st_size!=rows*width:
                assert not any(d['row_sha256']);self._remove(name)
            if not self._file(name).exists():
                assert not any(d['row_sha256']);self._reserve(name,rows*width)
            return d

    def pool(self,label,complete=False):
        with self.guard(False):
            d=self._get('pool_'+label+'.json');assert not d.get('retired')
            if complete:assert d['complete']
            return d

    def pool_row(self,label,e,raw):
        with self.guard():
            meta='pool_'+label+'.json';d=self._get(meta);assert not d.get('retired')
            assert len(raw)==d['row_bytes'] and 0<=e<d['rows']
            if d['row_sha256'][e] is not None:
                assert self._readrow(d,e)==raw;return
            assert not d['complete']
            self._writeat(d['name'],e*d['row_bytes'],raw,'pool_half')
            self._crash('pool_row_written');d['row_sha256'][e]=digest(raw)
            self._put(meta,d);self._crash('pool_progress_committed')

    def pool_read(self,label,e):
        with self.guard(False):
            d=self._get('pool_'+label+'.json');assert not d.get('retired') and d['row_sha256'][e]
            return self._readrow(d,e)

    def pool_finish(self,label):
        with self.guard():
            meta='pool_'+label+'.json';d=self._get(meta);assert not d.get('retired') and all(d['row_sha256'])
            info=self._info(d['name'],d['row_bytes'],d['rows'],d['row_sha256'])
            if d['complete']:assert d['sha256']==info['sha256'];return d
            d.update(info);d['complete']=True;self._put(meta,d);return d

    def pool_retire(self,label):
        """Only callers at a completed arithmetic barrier may retire a pool."""
        with self.guard():
            meta='pool_'+label+'.json';d=self._get(meta)
            if not d.get('retired'):
                assert d['complete']
                assert self._info(d['name'],d['row_bytes'],d['rows'],d['row_sha256'])['sha256']==d['sha256']
                if self._file('CURRENT.json').exists():
                    c=self._get('CURRENT.json');assert d['name'] not in (c['state']['name'],c['aux']['name'])
                d['retired']=True;self._put(meta,d);self._crash('pool_retirement_committed')
            self._remove(d['name'])

    def finish_initialization(self,authority):
        with self.guard():
            d=self._get('pool_initial.json');assert d['complete'] and not d.get('retired')
            info=self._info(d['name'],d['row_bytes'],d['rows'],d['row_sha256'])
            name='aux_initial.bin'
            if not self._file(name).exists():self._reserve(name,d['rows'])
            assert self._file(name).stat().st_size==d['rows']
            aux=self._info(name,1,d['rows']);assert all(x==digest(b'\0') for x in aux['row_sha256'])
            c={'tag':'initial','phase':'ready','epoch':0,'state':info,'aux':aux,'authority':authority}
            if self._file('CURRENT.json').exists():assert self._get('CURRENT.json')==c
            else:self._put('CURRENT.json',c)
            self._crash('initial_generation_committed');return c
