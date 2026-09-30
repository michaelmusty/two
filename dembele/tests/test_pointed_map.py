"""Independent exact controls for one-pole maps and CM trace normalization."""
import importlib.util
from pathlib import Path
import runpy
import unittest

import mpmath as mp
from sage.all import QQ, ComplexBallField, NumberField, PolynomialRing, PowerSeriesRing, matrix
from belyi.pointed_series import echelon

ROOT=Path(__file__).resolve().parents[2]
def module(name,filename):
    spec=importlib.util.spec_from_file_location(name,ROOT/'dembele/pari'/filename)
    result=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

maps=module('pointed_map_test','91_pointed_map.py')
cm=module('cm_fiber_test','92_cm_fibers.py')
model=module('pointed_model_test','93_pointed_map_model.py')


def genus_six_control():
    # Smooth trigonal curve y^3=x^7-x+1, genus 6, at the ordinary point (0,1).
    ring=PowerSeriesRing(QQ,'u',default_prec=100)
    u=ring.gen()
    x=QQ(2)/3*u
    y=(1-x+x**7)**(QQ(1)/3)
    forms=echelon([x**i/y**2 for i in range(4)]+[x**i/y for i in range(2)],list(range(6)))
    return forms,x,y


class PointedMapTests(unittest.TestCase):
    def test_exact_curve_map_agrees_with_independent_pole_cancellation(self):
        forms,x,y=genus_six_control()
        polynomials=PolynomialRing(ComplexBallField(330),'u')
        numeric=[polynomials(f.list()) for f in forms]
        with mp.workdps(90):
            constants,zero=maps.recover_map(numeric,6,96,64,rank_tolerance=1e-12)
            self.assertEqual(constants,[])
            result,report=maps.recover_map(numeric,7,96,64,rank_tolerance=1e-12)
            self.assertEqual(len(result),1)
            self.assertLess(report['solve']['held_out_scaled_residual_bound'],1e-75)
            # At infinity ord(x)=-3, ord(y)=-7. N/x^7 has no infinity
            # pole when 3*i+7*j<=21. Impose order-seven cancellation
            # at the other two points above x=0, independently of canonical products.
            ring=PolynomialRing(QQ,'z');z=ring.gen()
            field=NumberField(z*z+z+1,'zeta');zeta=field.gen()
            series=PowerSeriesRing(field,'t',default_prec=12);t=series.gen()
            branch=zeta*(1-t+t**7)**(QQ(1)/3)
            monomials=[(i,j) for j in range(3) for i in range(8) if 3*i+7*j<=21]
            evaluated=[t**i*branch**j for i,j in monomials]
            constraints=matrix(QQ,[[p[n][k] for p in evaluated] for n in range(7) for k in range(2)])
            kernel=constraints.right_kernel().basis()
            self.assertEqual(len(kernel),2)
            vector=next(v for v in kernel if sum(v[i] for i,(a,b) in enumerate(monomials) if a==0))
            expected=sum(c*x**i*y**j for c,(i,j) in zip(vector,monomials))/x**7
            got=[mp.mpc(*v) for v in result[0]['raw_coordinate_laurent_coefficients']]
            for n in range(14):
                if n==7: # Functions are unique only modulo constants.
                    continue
                rational=expected[n-7]/expected[-7]
                exact=mp.mpf(str(rational.numerator()))/mp.mpf(str(rational.denominator()))
                self.assertLess(abs(got[n]/got[0]-exact),mp.mpf('1e-70'))

    def test_failed_rank_is_not_reported_as_a_map(self):
        from dembele.tests.test_arithmetic_quadrics import genus_four_forms
        forms=genus_four_forms(100)
        u=forms[0].parent().gen()
        forms=echelon([f(u/2) for f in forms],list(range(4)))
        ring=PolynomialRing(ComplexBallField(250),'u')
        # These high-weight monomials do not span the required space.
        with self.assertRaisesRegex(ValueError,'numerical product ranks'):
            maps.recover_map([ring(f.list()) for f in forms],4,96,64,power=3)

    def test_exact_thesis_functions_and_trace_normalization(self):
        known=runpy.run_path(str(ROOT/'belyi/validate_q8.sage'))
        polynomial=known['f']
        ring=PolynomialRing(QQ,'s');s=ring.gen()
        base=NumberField(s*s-15,'a');a=base.gen()
        extension_ring=PolynomialRing(base,'z');z=extension_ring.gen()
        field=base.extension(z*z+1,'I');I=field.gen()
        series=PowerSeriesRing(base,'u',default_prec=24);u=series.gen()
        yy=a*(polynomial(1+u)/15)**(QQ(1)/2)
        roots=[field(0),field(1)/2,-field(1)/2,I/2,-I/2]
        self.assertTrue(all(polynomial(r)==0 for r in roots))
        # At P=(1,sqrt(15)), f3=(y+T2)/(x-1)^3 and f4=(y+T3)/(x-1)^4.
        # The conjugate numerators vanish to orders 3 and 4; degree
        # bounds give no pole at infinity. Thus these are global one-pole functions.
        truncations=[sum(yy[i]*u**i for i in range(m)) for m in [3,4]]
        for m,T in zip([3,4],truncations):
            self.assertGreaterEqual((T-yy).valuation(),m)
            self.assertEqual(((T+yy)/u**m).valuation(),-m)
        values=[]
        for m in [3,4]:
            values.append([sum(field(yy[i])*(r-1)**i for i in range(m))/(r-1)**m for r in roots])
        xx,zz,normal=cm.trace_normalization(*values)
        self.assertEqual(sum(xx),0)
        self.assertEqual(sum(zz),0)
        self.assertEqual(sum(x*y for x,y in zip(xx,zz)),0)
        self.assertEqual(sum(x*x for x in xx),sum(x**3 for x in xx))
        self.assertEqual(sum(x*x for x in zz),sum(x**3 for x in zz))
        self.assertTrue(all(c[1]==0 for c in normal.values()))
        xunit=[(yy+truncations[0])[i] for i in range(20)]
        yunit=[(yy+truncations[1])[i] for i in range(20)]
        ax,ay,t=cm.normalized_laurent(xunit,yunit,3,4,normal,length=20)
        self.assertEqual(t[0],0)
        self.assertNotEqual(t[1],0)
        self.assertEqual(t[1],ax[0]/ay[0])

    def test_trace_coordinates_are_invariant_under_complex_triangular_changes(self):
        ring=PolynomialRing(QQ,'z');z=ring.gen();field=NumberField(z*z+1,'I');I=field.gen()
        xs=[field(v) for v in [0,1,2,4,9]]
        ys=[field(v) for v in [1,3,8,-2,7]]
        expected_x,expected_y,_=cm.trace_normalization(xs,ys)
        new_x=[(2+I)*x+3-I for x in xs]
        new_y=[(1-2*I)*y+(3+I)*x+7 for x,y in zip(xs,ys)]
        xx,yy,_=cm.trace_normalization(new_x,new_y)
        self.assertEqual(xx,expected_x)
        self.assertEqual(yy,expected_y)

    def test_symmetric_cm_values_do_not_silently_choose_a_root(self):
        with self.assertRaisesRegex(ValueError,'zero second or third moment'):
            cm.trace_normalization([QQ(-1),QQ(0),QQ(1)],[QQ(1),QQ(2),QQ(4)])

    def test_weighted_plane_relation_on_thesis_curve_uses_unused_jets(self):
        ring=PolynomialRing(QQ,'z');z=ring.gen();field=NumberField(z*z-15,'a');a=field.gen()
        series=PowerSeriesRing(field,'u',default_prec=48);u=series.gen()
        y=a*((16*(1+u)**5-(1+u))/15)**(QQ(1)/2)
        T2=sum(y[i]*u**i for i in range(3))
        T3=sum(y[i]*u**i for i in range(4))
        polynomials=PolynomialRing(field,'u')
        support,columns=model.weighted_columns(polynomials((y+T2).list()),
            polynomials((y+T3).list()),polynomials(1),3,4,40)
        self.assertEqual(len(support),11)
        fitted=matrix(field,[[p[n] for p in columns] for n in range(13)])
        kernel=fitted.right_kernel()
        self.assertEqual(kernel.dimension(),1)
        relation=kernel.basis()[0]
        unused=matrix(field,[[p[n] for p in columns] for n in range(13,40)])
        self.assertTrue((unused*relation).is_zero())
        coefficients,residual,rows=model.triangular_relation(support,columns,3,4,40)
        self.assertTrue(residual.is_zero())
        self.assertEqual(len(rows),10)
        expected=relation/relation[support.index((0,3))]
        self.assertEqual(coefficients,list(expected))
        balls=ComplexBallField(330)
        root=balls(15).sqrt()
        embedding=lambda c: balls(c[0])+root*balls(c[1])
        ball_ring=PolynomialRing(balls,'u')
        numeric=[ball_ring([embedding(c) for c in p.list()]) for p in columns]
        with mp.workdps(90):
            fitted,residual,details=model.balanced_relation(numeric,20,40,.5,support.index((0,3)))
            for got,want in zip(fitted,expected):
                self.assertLess(float(abs(got-embedding(want)).upper()),1e-70)
            checked=model.relation_diagnostics(fitted,residual,numeric,details['interpolation_rows'],20,40)
            self.assertTrue(checked['passes_empirical_residual_screen'])
            # Changing only an unused coefficient must invalidate the equation.
            perturbation=balls(sum(abs(c*p[39]).upper() for c,p in zip(fitted,numeric)))
            numeric[support.index((0,3))]+=perturbation*ball_ring.gen()**39
            fitted,residual,details=model.balanced_relation(numeric,20,40,.5,support.index((0,3)))
            checked=model.relation_diagnostics(fitted,residual,numeric,details['interpolation_rows'],20,40)
            self.assertFalse(checked['passes_empirical_residual_screen'])


if __name__=='__main__':
    unittest.main()
