"""Numerically reconstruct the order-32 CM-centered Dirichlet sector."""
import importlib
import json
from pathlib import Path
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull

pilot = importlib.import_module('68_cm_differentials')
q, _, delta = pilot.load_actions()
normal = ((q/(1-delta))[:,None]*np.exp(2j*np.pi*np.arange(32)/32)[None,:]).ravel()
halfspaces = np.column_stack([normal.real,normal.imag,-np.ones(len(normal))])
angle = 2*np.pi/32
halfspaces = np.vstack([halfspaces,[0,-1,0],[-np.sin(angle),np.cos(angle),0]])
interior = .1*np.array([np.cos(angle/2),np.sin(angle/2)])
vertices = HalfspaceIntersection(halfspaces,interior).intersections
vertices = vertices[ConvexHull(vertices).vertices]
klein = vertices[:,0]+1j*vertices[:,1]
assert np.max(abs(klein))<1
disk = klein/(1+np.sqrt(1-abs(klein)**2))
previous, following = np.roll(disk,1),np.roll(disk,-1)
u=(previous-disk)/(1-disk.conjugate()*previous)
v=(following-disk)/(1-disk.conjugate()*following)
angles=abs(np.angle(u/v))
area=(len(disk)-2)*np.pi-sum(angles)
assert abs(area/(2*np.pi)-1455/32)<1e-6
report={'vertices':len(disk),'max_disk_radius':float(max(abs(disk))),
        'area_over_2pi':float(area/(2*np.pi)),'expected_area_over_2pi':1455/32,
        'area_absolute_error':float(abs(area/(2*np.pi)-1455/32)),
        'disk_vertices':[[float(z.real),float(z.imag)] for z in disk],
        'status':'numerical consistency check; not an interval certificate'}
out=Path(__file__).resolve().parents[1]/'data/computed/cm_sector.json'
out.write_text(json.dumps(report,indent=2)+'\n')
print(f'PASS|69_cm_sector: {len(disk)} vertices; radius {max(abs(disk)):.14f}; area/(2pi) {area/(2*np.pi):.11f}')
