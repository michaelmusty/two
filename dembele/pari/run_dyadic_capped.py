"""Persistent wrapper for the project's 180-second dyadic job protocol.

Usage: python3 dembele/pari/run_dyadic_capped.py DRIVER STEM PASS_MARKER [ARGS...]
STEM names new log/receipt files in dembele/data/computed. Never overwrite.
"""
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import sys

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('bounded',ROOT/'dembele/pari/272_cm_frame_bounded_jobs.py')
b=importlib.util.module_from_spec(s);s.loader.exec_module(b)


def main():
    assert len(sys.argv)>=4,__doc__
    driver=(ROOT/sys.argv[1]).resolve();stem=sys.argv[2];marker=sys.argv[3]
    assert driver.is_file() and driver.is_relative_to(ROOT)
    assert re.fullmatch(r'[A-Za-z0-9_-]+',stem)
    receipt=DATA/(stem+'.job.json');log=DATA/(stem+'.log')
    assert not receipt.exists() and not log.exists()
    original=b.source(driver);env=dict(os.environ);env['OPENBLAS_NUM_THREADS']='1'
    job=b.run_job(['python3',str(driver)]+sys.argv[4:],log,180,marker,env=env)
    job['driver']=original;job['sources'].append(b.source(Path(__file__)))
    if job['status']!='pass':
        snapshot=DATA/(stem+'_failed.py');assert not snapshot.exists()
        shutil.copyfile(driver,snapshot);job['failed_driver_snapshot']=b.source(snapshot)
    receipt.write_text(json.dumps(job,indent=2)+'\n');print(json.dumps(job,indent=2),flush=True)
    return 0 if job['status']=='pass' else 1


if __name__=='__main__':raise SystemExit(main())
