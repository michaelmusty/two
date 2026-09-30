"""D85 native-ring control for the precision-aware matrix inverse."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("inverse128_driver", ROOT / "dembele/pari/287_cm_frame_cubic_precision128_memory.py")
driver = importlib.util.module_from_spec(spec); spec.loader.exec_module(driver)
script = ROOT / "dembele/magma/288_cm_frame_memory_arithmetic_check.m"
base = DATA / "cm_frame_memory_arithmetic_check"
job, jpath = driver.run(script, base, "PASS|288_MEMORY_ARITHMETIC", [Path(__file__)], "")
result = {"status": "pass", "milestone": "D85", "precision_digits": 128,
          "sources": [driver.checks.source(p) for p in (Path(__file__), jpath)],
          "matrix_sizes": [1,4,9,16,32], "native_inverse_equality_verified": True, "native_pointwise_scaling_verified": True,
          "highest_digit_inverse_corruption_rejected": True}
path = base.with_suffix(".json")
if path.exists():
    assert json.loads(path.read_text()) == result
else:
    path.write_text(json.dumps(result, indent=2)+"\n")
print("PASS|288_MEMORY_ARITHMETIC_CHECK", round(job["wall_seconds"],3))
