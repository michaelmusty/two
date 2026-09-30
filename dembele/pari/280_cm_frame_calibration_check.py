"""D84: independently check exact synthetic recoveries using plain integer arithmetic."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
POLYNOMIAL = [2, 0, -16, 0, 20, 0, -8, 0, 1]


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def product(a, b):
    out = [0]*15
    for i in range(8):
        for j in range(8):
            out[i+j] += a[i]*b[j]
    for i in range(14, 7, -1):
        coefficient = out[i]
        for j in range(9):
            out[i-8+j] -= coefficient*POLYNOMIAL[j]
    assert not any(out[8:])
    return out[:8]


def main():
    summaries, sources = [], [source(Path(__file__))]
    exact_recoveries, failed_searches = 0, 0
    for path in sorted(DATA.glob("cm_frame_recognition_calibration_*.json")):
        if path.name.endswith("_job.json"):
            continue
        record = json.loads(path.read_text())
        assert record["status"] == "pass" and record["synthetic_only"]
        for item in record["sources"]:
            assert source(item["path"]) == item
        n, train, root = record["precision_digits"], record["training_digits"], record["root_mod_precision"]
        modulus = 31**n
        assert sum(c*pow(root, i, modulus) for i, c in enumerate(POLYNOMIAL)) % modulus == 0
        assert root % 31 == record["root_mod31"]
        for result in record["results"]:
            known, values, anchor = result["known_coordinates"], result["values"], result["anchor"]
            assert len(known) == len(values) == 25 and all(len(row) == 8 for row in known)
            assert max(abs(c) for row in known for c in row) == result["input_height"] == 10**result["exponent"]
            assert math.gcd(*(c for row in known for c in row)) == 1
            scale = result["common_padic_scale"]
            assert scale % 31 != 0 and values[anchor] % 31 != 0
            actual = [scale*sum(row[j]*pow(root, j, modulus) for j in range(8)) % modulus for row in known]
            assert actual == values
            assert result["recovered"] == (result["survivor_count"] > 0)
            if result["recovered"]:
                recovered = result["first_survivor"]["row"]
                assert len(recovered) == 200
                point = [recovered[8*i:8*i+8] for i in range(25)]
                assert all(product(point[i], known[anchor]) == product(point[anchor], known[i]) for i in range(25))
                ev = [sum(row[j]*pow(root, j, modulus) for j in range(8)) % modulus for row in point]
                assert ev[anchor] % 31 != 0
                assert all((ev[i]*values[anchor]-ev[anchor]*values[i]) % modulus == 0 for i in range(25))
                # Independent rejection of a changed first-unused digit.
                changed = list(values)
                index = next(i for i in range(25) if i != anchor)
                changed[index] = (changed[index]+31**train) % modulus
                assert any((ev[i]*changed[anchor]-ev[anchor]*changed[i]) % modulus for i in range(25))
                exact_recoveries += 1
            else:
                assert result["first_survivor"] is None
                failed_searches += 1
            summaries.append({"digits": n, "train": train, "seed": record["seed"],
                              "root": record["root_mod31"], "height": result["input_height"],
                              "recovered": result["recovered"], "survivors": result["survivor_count"]})
        sources.append(source(path))
    assert summaries and exact_recoveries > 0 and failed_searches > 0
    output = {"status": "pass", "milestone": "D84", "sources": sources,
              "synthetic_cases": len(summaries), "exact_recoveries_independently_checked": exact_recoveries,
              "failed_basis_row_searches": failed_searches, "cases": summaries,
              "target_height_bound_claimed": False, "uniform_recovery_guarantee_claimed": False}
    path = DATA / "cm_frame_recognition_calibration_check.json"
    assert not path.exists(), "Do not overwrite an already bound calibration audit."
    path.write_text(json.dumps(output, indent=2)+"\n")
    print("PASS|280_CALIBRATION_CHECK", len(summaries), exact_recoveries, failed_searches)


if __name__ == "__main__":
    main()
