# D86 transport adapter; original 304 SHA256 204abe74d83fd269dc4363cd14e9d10ed05f01650f37ed3555b4fa9b5a4b62a5
"""D86: resume frozen remote stages through transient transport failures.

Only the idempotent Python transfer/status operations of 299 are retried.
The detached worker launch still uses its original durable-state guard and
is never retried here. Completed mathematical jobs retain their receipts.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from http.client import IncompleteRead
from ssl import SSLEOFError

ROOT = Path(__file__).resolve().parents[2]
PARI = ROOT / "dembele/pari"
DATA = ROOT / "dembele/data/computed"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage")
    parser.add_argument("--family", choices=("class", "pointed", "adjoint"))
    args = parser.parse_args()
    assert (args.stage is None) != (args.family is None)
    filename = "302_cm_frame_cubic128_parallel_checks.py" if args.family else "300_cm_frame_cubic_precision128_chatelet.py"
    spec = importlib.util.spec_from_file_location("resumed_chatelet_stage", PARI / filename)
    entry = importlib.util.module_from_spec(spec); spec.loader.exec_module(entry)
    remote = entry.remote if args.family else entry
    remote.driver.PROCESS_SOURCES.extend((Path(__file__), PARI / "304_cm_frame_chatelet_resume.py"))
    original = remote.transport.python

    def resilient_python(code, **kwargs):
        for attempt in range(6):
            try:
                return original(code, **kwargs)
            except (URLError, TimeoutError, ConnectionError, IncompleteRead, SSLEOFError, RuntimeError) as error:
                transient = (isinstance(error, (URLError, TimeoutError, ConnectionError, IncompleteRead, SSLEOFError))
                             or str(error).startswith("Chatelet socket timeout")
                             or any(str(error).startswith("CoCalc HTTP "+str(code)+":") for code in (429, 502, 503, 504)))
                if isinstance(error, HTTPError):
                    transient = error.code in (429, 502, 503, 504)
                if not transient:
                    raise
                event = {"status": "transient_transport_error", "epoch_ns": time.time_ns(),
                    "attempt": attempt+1, "maximum_attempts": 6,
                    "operation_sha256": hashlib.sha256(code.encode()).hexdigest(),
                    "error_type": type(error).__name__,
                    "scope": "Idempotent mathematical transfer or status operation; no job launch retry",
                    "source": remote.checks.source(Path(__file__))}
                text = json.dumps(event, indent=2)+"\n"
                path = DATA / "chatelet_d86_128" / ("transport_event_"+hashlib.sha256(text.encode()).hexdigest()[:16]+".json")
                remote.driver.immutable(path, text)
                remote.driver.PROCESS_SOURCES.append(path)
                print("CHATELET_TRANSIENT_TRANSPORT", type(error).__name__, attempt+1, "/ 6", flush=True)
                if attempt == 5:
                    raise
                time.sleep(min(5*2**attempt, 40))

    remote.transport.python = resilient_python
    sys.argv = [str(PARI / filename), "--family", args.family] if args.family else [str(PARI / filename), "--stage", args.stage]
    entry.main()


if __name__ == "__main__":
    main()
