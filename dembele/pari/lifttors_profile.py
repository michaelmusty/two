"""Insert checked diagnostic hooks into copies of the D66 C sources.

No arithmetic statement, precision step, random call, or reclamation point
is removed or reordered. Returns evaluate their original expression before
recording a checkpoint. Comments/string literals are masked for C scanning.
"""
import re

from lifttors_lift import replace_once


def code_mask(text):
    return re.sub(r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',
                  lambda m: "".join("\n" if c == "\n" else " " for c in m[0]),
                  text, flags=re.S)


def instrument(text, name, precision, hooks=(), return_type="GEN"):
    mask = code_mask(text)
    definitions = list(re.finditer(r'\b' + return_type + r'\s+' + name + r'\s*\([^;{}]*\)\s*\{', mask))
    if len(definitions) != 1:
        raise ValueError(f"Expected one live definition of {name}")
    match = definitions[0]
    start = match.end()-1
    depth = 1
    end = start+1
    while depth:
        depth += (mask[end] == "{") - (mask[end] == "}")
        end += 1
    body = text[start+1:end-1]
    masked = code_mask(body)
    returns = list(re.finditer(r'\breturn\s+([^;]+);', masked))
    if not returns:
        raise ValueError(f"No returns in {name}")
    end_function = "LiftProfileEnd" if return_type == "GEN" else "LiftProfileEndU"
    for item in reversed(returns):
        expression = body[item.start(1):item.end(1)]
        body = body[:item.start()] + f"return {end_function}(&d67_frame,({expression}));" + body[item.end():]
    for anchor, stage, object_name, e in hooks:
        body = replace_once(body, anchor, anchor +
                            f'\n    LiftProfilePoint(&d67_frame,"{stage}",{object_name},{e});')
    body = f'\n    LiftProfileFrame d67_frame;\n    LiftProfileStart(&d67_frame,"{name}",{precision});\n' + body
    return text[:start+1] + body + text[end-1:]


def profile_pic(text):
    for name in ["PicRed", "PicNeg", "PicChord", "PicMul"]:
        hooks = []
        if name == "PicChord":
            hooks = [
                ("WAWB = DivAdd(WA,WB,2*d0+1-g,T,p,e,pe,0);", "product_space", "WAWB", "e"),
                ("WAB = DivSub(V1,WAWB,KV3,d0+1-g,T,p,e,pe,2);", "first_division", "WAB", "e"),
                ("sV = DivMul(s,V,T,pe);", "section_product", "sV", "e"),
                ("WC = DivSub(WAB,sV,KV,d0+1-g,T,p,e,pe,2);", "second_division", "WC", "e"),
            ]
        text = instrument(text, name, "e" if name == "PicRed" else "Jgete(J)", hooks)
    text = instrument(text, "DivAdd", "e", [
        ("WAB = FqM_image(WAB,T,p);", "image_selected", "WAB", "e"),
    ])
    # The checkpoint must precede image computation, while the uncollected
    # random combinations and products are still on the PARI stack.
    anchor = "\t\tWAB = FqM_image(WAB,T,p);"
    text = replace_once(text, anchor, '    LiftProfilePoint(&d67_frame,"products_before_image",WAB,e);\n' + anchor)
    text = instrument(text, "DivSub", "e", [
        ("KB = mateqnpadic(WB,T,pe,p,e);", "equations_of_WB", "KB", "e"),
        ("res = matkerpadic(K,T,pe,p,e);", "kernel_returned", "res", "e"),
    ])
    anchor = "\t\tres = matkerpadic(K,T,pe,p,e);"
    text = replace_once(text, anchor, '    LiftProfilePoint(&d67_frame,"constraints_before_kernel",K,e);\n' + anchor)
    return '#include "lifttors_profile.h"\n' + text


def profile_lift(text):
    text = instrument(text, "PicDeflate_U", "Jgete(J)")
    text = instrument(text, "PicInflate_U", "Jgete(J)", [
        ("GWV = FqM_image(GWV,T,p);", "image_selected", "GWV", "e"),
        ("W = DivSub(V,GWV,KV,nW,T,p,e,pe,3);", "division_returned", "W", "e"),
    ])
    text = instrument(text, "PicLiftTors", "Jgete(J)", [
        ("U0 = matkerpadic(Vs,T,pefin2,p,efin2);", "tangent_basis", "U0", "efin2"),
        ("J1 = PicRed(J,e1);", "initial_reduced_J", "J1", "e1"),
        ("U = gerepileupto(av1,U);", "initial_deflation_collected", "U", "e1"),
        ("J2 = e2<efin ? PicRed(J,e2) : J;", "iteration_J", "J2", "e2"),
        ("avrho = avma;", "product_matrix", "GWV", "e2"),
        ("Ainv = ZpXQMinv(gel(ABCD,1),T,pe2,p,e2);", "schur_inverse", "Ainv", "e2"),
        ("CAinv = FqM_mul(gel(ABCD,3),Ainv,T,pe2);", "schur_left", "CAinv", "e2"),
        ("AinvB = FqM_mul(Ainv,gel(ABCD,2),T,pe2);", "schur_right", "AinvB", "e2"),
        ("KM = LiftRowsMatker(V,U0,uv,AinvB,CAinv,rho,T,pe21,p,e21);", "row_kernel_returned", "KM", "e21"),
        ("KM = gerepileupto(avrho,KM);", "schur_collected", "KM", "e2"),
        ("W = PicInflate_U(J2,U,NULL);\n\t\t\tW = gerepileupto(av2,W);", "inflation_collected", "W", "e2"),
        ("W = PicMul(J2,W,pe21,0);", "multiplication_returned", "W", "e2"),
    ])
    return '#include "lifttors_profile.h"\n' + text


def profile_linalg(text):
    for name in ["matkerpadic", "mateqnpadic"]:
        text = instrument(text, name, "e", [
            ("IJ = FqM_indexrank(A,T,p);", "rank_selected", "NULL", "e"),
            ("B = gerepileupto(av1,ZpXQMinv(A1,T,pe,p,e));", "inverse_collected", "B", "e"),
        ])
    return '#include "lifttors_profile.h"\n' + text


def profile_validator(text):
    text = instrument(text, "DivSub_dimval", "e", [
        ("KB=mateqnpadic(WB,T,pe,p,e);", "equations_of_WB", "KB", "e"),
        ("\n    L=matkerpadic(R,T,pe,p,e);", "initial_kernel", "L", "e"),
        ("gerepileall(keep,2,&R,&L);", "selected_rows_collected", "NULL", "e"),
    ], return_type="ulong")
    return '#include "lifttors_profile.h"\n' + text
