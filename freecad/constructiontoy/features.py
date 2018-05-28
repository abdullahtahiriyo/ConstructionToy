# -*- coding: utf-8 -*-
#***************************************************************************
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

from __future__ import division
import os

import numpy as np

import FreeCAD as App
import Part
from Part import BSplineCurve, Shape, Wire, Face, makePolygon, \
    BRepOffsetAPI, Shell, makeLoft, Solid, LineSegment, BSplineSurface, makeCompound,\
     show, makePolygon, makeHelix, makeSweepSurface, makeShell, makeSolid




__all__=["plate"]



def fcvec(x):
    if len(x) == 2:
        return(App.Vector(x[0], x[1], 0))
    else:
        return(App.Vector(x[0], x[1], x[2]))

class ViewProviderConstructionToy:
    def __init__(self, obj):
        ''' Set this object to the proxy object of the actual view provider '''
        obj.Proxy = self

    def attach(self, vobj):
        self.vobj = vobj

    def getIcon(self):
        __dirname__ = os.path.dirname(__file__)
        return(os.path.join(__dirname__, "icons", "createplate.svg"))

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


class plate(object):

    """ Construction Toy plate"""

    def __init__(self, obj):
        obj.addProperty("App::PropertyInteger",
                        "xoccurrences", "Plate", "number of modules in x")
        obj.addProperty("App::PropertyInteger",
                        "yoccurrences", "Plate", "number of modules in y")
        obj.addProperty(
            "App::PropertyLength", "fillet", "Plate", "fillet radius")
        obj.addProperty(
            "App::PropertyLength", "xsize", "Module", "size in x")
        obj.addProperty(
            "App::PropertyLength", "ysize", "Module", "size in y")
        obj.addProperty(
            "App::PropertyLength", "height", "Module", "height")
        obj.addProperty(
            "App::PropertyLength", "holesize", "Module", "hole diameter")

        obj.xoccurrences = 3
        obj.yoccurrences = 1
        obj.xsize = '30 mm'
        obj.ysize = '24 mm'
        obj.height = '5 mm'
        obj.holesize = '11 mm'
	obj.fillet = '1 mm'
        self.obj = obj
        obj.Proxy = self

    def execute(self, fp):
	xtotal = fp.xsize.Value * fp.xoccurrences
	ytotal = fp.ysize.Value * fp.yoccurrences

	#App.Console.PrintMessage("xtotal,ytotal:" + str(xtotal) + "," + str(ytotal) + "\n")

    	e1 = LineSegment(App.Vector(0, 0, 0), App.Vector(xtotal, 0, 0)).toShape().Edges[0]
    	e2 = LineSegment(App.Vector(xtotal, 0, 0), App.Vector(xtotal, ytotal, 0)).toShape().Edges[0]
    	e3 = LineSegment(App.Vector(xtotal, ytotal, 0), App.Vector(0, ytotal, 0)).toShape().Edges[0]
    	e4 = LineSegment(App.Vector(0, ytotal, 0), App.Vector(0, 0, 0)).toShape().Edges[0]
    	w = Wire([e1, e2, e3, e4])

	#hole
	holes = []
	for i in range(fp.xoccurrences):
		for j in range(fp.yoccurrences):
			holes.append(Part.Wire(Part.makeCircle(fp.holesize.Value/2, App.Vector(fp.xsize.Value/2 + i*fp.xsize.Value, fp.ysize.Value/2 + j*fp.ysize.Value, 0),App.Vector(0, 0, -1))))

        face = Part.Face([w] + holes)
	baseshape = face.extrude(App.Vector(0, 0, fp.height.Value))
	if fp.fillet.Value > 0:
		borders = []
		for i in range(12):
			borders.append(baseshape.Edges[i])
        	fp.Shape = baseshape.makeFillet(fp.fillet.Value, borders)
	else:
        	fp.Shape = face.extrude(App.Vector(0, 0, fp.height.Value))


    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

def helicalextrusion(wire, height, angle, double_helix = False):
    direction = bool(angle < 0)
    if double_helix:
        first_spine = makeHelix(height * 2. * np.pi / abs(angle), 0.5 * height, 10., 0, direction)
        first_solid = first_spine.makePipeShell([wire], True, True)
        second_solid = first_solid.mirror(fcvec([0.,0.,0.]), fcvec([0,0,1]))
        faces = first_solid.Faces + second_solid.Faces
        faces = [f for f in faces if not on_mirror_plane(f, 0., fcvec([0., 0., 1.]))]
        solid = makeSolid(makeShell(faces))
        mat = App.Matrix()
        mat.move(fcvec([0, 0, 0.5 * height]))
        return solid.transformGeometry(mat)
    else:
        first_spine = makeHelix(height * 2 * np.pi / abs(angle), height, 10., 0, direction)
        first_solid = first_spine.makePipeShell([wire], True, True)
        return first_solid


def make_face(edge1, edge2):
    v1, v2 = edge1.Vertexes
    v3, v4 = edge2.Vertexes
    e1 = Wire(edge1)
    e2 = Line(v1.Point, v3.Point).toShape().Edges[0]
    e3 = edge2
    e4 = Line(v4.Point, v2.Point).toShape().Edges[0]
    w = Wire([e3, e4, e1, e2])
    return(Face(w))


def makeBSplineWire(pts):
    wi = []
    for i in pts:
        out = BSplineCurve()
        out.interpolate(list(map(fcvec, i)))
        wi.append(out.toShape())
    return Wire(wi)

def on_mirror_plane(face, z, direction, small_size=0.000001):
    # the tolerance is very high. Maybe there is a bug in Part.makeHelix.
    return (face.normalAt(0, 0).cross(direction).Length < small_size and
            abs(face.CenterOfMass.z - z)  < small_size)
