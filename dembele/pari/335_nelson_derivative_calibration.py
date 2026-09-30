"""D91: independent rational calibration after differentiating the kernel.

At Y=0, the Lie derivative delta1 delta2 of e^(2i arg X) W2(4pi|X|)
is W2 - A*dW2/dA, A=|X|^2. This checks the absolute-X powers in the
Mellin implementation, not merely its undifferentiated Bessel formula.
"""
import hashlib
import json
from pathlib import Path
import mpmath as mp

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/"dembele/data/computed"


def main():
    mp.mp.dps=60;records=[]
    for absolute_X in [mp.mpf("0.7"),mp.mpf("1.3"),mp.mpf("2")]:
        A=absolute_X**2
        def W2(a):
            x=4*mp.pi*mp.sqrt(a)
            return (x*mp.besselk(1,x)-mp.besselk(2,x))/2
        direct=W2(A)-A*mp.diff(W2,A)
        z=4*mp.pi**2*A;c=mp.mpf("1.25")
        def integrand(t):
            s=c+1j*t
            return mp.re((2*s-1)*mp.gamma(s)*mp.gamma(s+3)*z**(-s))
        # One auxiliary term, and one signed quaternion term. No factor 2
        # for +/- here. Vertical tails are not certified in this diagnostic.
        mellin=mp.quad(integrand,[0,1,2,4,8,16,32,48,64])/mp.pi/(16*mp.pi**2*A)
        x=4*mp.pi*absolute_X
        W3=(x*mp.besselk(2,x)-mp.besselk(3,x))/4
        closed=4*mp.pi*absolute_X*W3
        err=abs(mellin-direct)/abs(direct)
        assert err<mp.mpf("1e-40") and abs(closed-direct)<abs(direct)*mp.mpf("1e-50")
        # The literal arXiv-v1 display (11) gives 4*pi*W3 at Y=0.
        # It differs by |X| in this direct local derivative test. We retain
        # the differentiated Gaussian calculation and record the discrepancy.
        literal=4*mp.pi*W3
        assert abs(direct/literal-absolute_X)<mp.mpf("1e-50")
        records.append({"absolute_X":str(absolute_X),"direct_derivative":mp.nstr(direct,45),
                        "Mellin_relative_error":mp.nstr(err,8),
                        "direct_over_literal_arxiv_v1_display":mp.nstr(direct/literal,30)})
    result={"status":"pass: rational (1,1) derivative calibration",
            "identity":"delta1 delta2 [phase2 W2(4*pi*sqrt(A))] at Y=0 = W2-A*dW2/dA = 4*pi*sqrt(A)*W3",
            "tests":records,"numerical_calibration_not_interval_proof":True,
            "arxiv_v1_display_11_scale_discrepancy":True,
            "published_2015_display_checked":False,
            "implementation_uses_direct_Gaussian_derivatives":True,
            "sources":[{"path":str(Path(__file__).relative_to(ROOT)),
                        "sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}]}
    output=DATA/"nelson_derivative_calibration_d91.json";assert not output.exists()
    output.write_text(json.dumps(result,indent=2)+"\n")
    print("Rational derivative relative errors:",[r["Mellin_relative_error"] for r in records])
    print("PASS|335_nelson_derivative_calibration")


if __name__=="__main__":main()
