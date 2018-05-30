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
import os, math

import numpy as np
import screw_maker2_2

import FreeCAD as App

from FreeCAD import Base

import Part
from Part import BSplineCurve, Shape, Wire, Face, makePolygon, \
    BRepOffsetAPI, Shell, makeLoft, Solid, LineSegment, BSplineSurface, makeCompound,\
     show, makePolygon, makeHelix, makeSweepSurface, makeShell, makeSolid

__all__=["plate", "separator", "washer", "screw"]


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
        return self.vobj.Object.Proxy.getIcon()

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

    def getIcon(self):
        __dirname__ = os.path.dirname(__file__)
        return(os.path.join(__dirname__, "icons", "createplate.svg"))

class separator(object):

    """ Construction Toy plate"""

    def __init__(self, obj):
        obj.addProperty(
            "App::PropertyLength", "outerdiameter", "Separator", "outer diameter")
	obj.addProperty(
            "App::PropertyLength", "fillet", "Separator", "fillet radius")
        obj.addProperty(
            "App::PropertyLength", "height", "Module", "height")
        obj.addProperty(
            "App::PropertyLength", "holesize", "Module", "hole diameter")

        obj.height = '32 mm'
        obj.outerdiameter = '19 mm'
        obj.holesize = '11 mm'
	obj.fillet = '1 mm'
        self.obj = obj
        obj.Proxy = self

    def execute(self, fp):

    	w = Part.Wire(Part.makeCircle(fp.outerdiameter.Value/2))
	#hole
	h = Part.Wire(Part.makeCircle(fp.holesize.Value/2, App.Vector(0, 0, 0), App.Vector(0, 0, -1)))

	face = Part.Face([w, h])

	baseshape = face.extrude(App.Vector(0, 0, fp.height.Value))

	if fp.fillet.Value > 0:
		borders = []
		for i in range(1,3):
			borders.append(baseshape.Edges[i])
        	fp.Shape = baseshape.makeFillet(fp.fillet.Value, borders)
	else:
        	fp.Shape = face.extrude(App.Vector(0, 0, fp.height.Value))


    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

    def getIcon(self):
        __dirname__ = os.path.dirname(__file__)
        return(os.path.join(__dirname__, "icons", "createseparator.svg"))

class washer(separator):
    """ Construction Toy washer"""

    def __init__(self, obj):
	separator.__init__(self,obj)
	obj.height = '5 mm'
	self.obj = obj
	obj.Proxy = self

    def getIcon(self):
        __dirname__ = os.path.dirname(__file__)
        return(os.path.join(__dirname__, "icons", "createwasher.svg"))

class screw(object):

    """ Construction Toy screw"""

    def __init__(self, obj):
        obj.addProperty(
            "App::PropertyLength", "height", "Screw", "length")
        obj.addProperty(
            "App::PropertyLength", "shanklength", "Screw", "shank length")
        obj.addProperty(
            "App::PropertyLength", "screwdiameter", "Screw", "diameter")
        obj.addProperty(
            "App::PropertyLength", "screwpitch", "Screw", "pitch")
        obj.addProperty(
            "App::PropertyBool", "chamfer", "Screw", "chamfer thread")
	obj.addProperty(
            "App::PropertyLength", "fillet", "Screw", "fillet radius")
        obj.addProperty(
            "App::PropertyLength", "outerdiameter", "Screw Head", "outer diameter")
        obj.addProperty(
            "App::PropertyLength", "headheight", "Screw Head", "height")
        obj.addProperty(
            "App::PropertyLength", "internaldiameter", "Screw Head", "cross hole diameter")
        obj.addProperty(
            "App::PropertyLength", "crosswidth", "Screw Head", "cross slot width")
        obj.addProperty(
            "App::PropertyLength", "crossdepth", "Screw Head", "cross slot depth")

	obj.height = '30 mm'
	obj.shanklength = '0 mm'
	obj.screwdiameter = '9.4 mm'
	obj.screwpitch = '2 mm'
	obj.fillet = '1 mm'
	obj.outerdiameter = '18.5 mm'
	obj.headheight = '8 mm'
	obj.internaldiameter = '9.4 mm'
	obj.crosswidth = '3 mm'
	obj.crossdepth = '4 mm'
	obj.chamfer = True

        self.Tuner = 510

        self.obj = obj
        obj.Proxy = self

    def execute(self, fp):

  	o = screw_maker2_2.Screw()
  	t = screw_maker2_2.Screw.setThreadType(o,'real')

	l = fp.height.Value
	P = fp.screwpitch.Value;
	c = 0.5
	dia = fp.screwdiameter.Value;
	dw = 1.5 * dia
	e = fp.outerdiameter.Value;
	k = fp.headheight.Value;
	r = 0.5
	s = 0.9 * e

    	residue, turns = math.modf((l-1*P)/P)
      	halfturns = 2*int(turns)

    	if residue < 0.5:
      		a = l - (turns+1.0) * P 
      		halfturns = halfturns +1
    	else:
      		halfturns = halfturns + 2
      		a = l - (turns+2.0) * P

	offSet = r - a

    	sqrt2_ = 1.0/math.sqrt(2.0)
    	cham = (e-s)*math.sin(math.radians(15)) # needed for chamfer at head top

    	#Head Points  Usage of k, s, cham, c, dw, dia, r, a
    	#FreeCAD.Console.PrintMessage("der Kopf mit halfturns: " + str(halfturns) + "\n")
    	Pnt0 = Base.Vector(0.0,0.0,k)
    	Pnt2 = Base.Vector(s/2.0,0.0,k)
    	Pnt3 = Base.Vector(s/math.sqrt(3.0),0.0,k-cham)
    	Pnt4 = Base.Vector(s/math.sqrt(3.0),0.0,c)
    	Pnt5 = Base.Vector(dw/2.0,0.0,c)
    	Pnt6 = Base.Vector(dw/2.0,0.0,0.0)
    	Pnt7 = Base.Vector(dia/2.0+r,0.0,0.0)     #start of fillet between head and shank
    	Pnt8 = Base.Vector(dia/2.0+r-r*sqrt2_,0.0,-r+r*sqrt2_) #arc-point of fillet
    	Pnt9 = Base.Vector(dia/2.0,0.0,-r)        # end of fillet
    	Pnt10 = Base.Vector(dia/2.0,0.0,-a)        # Start of thread

    	edge1 = Part.makeLine(Pnt0,Pnt2)
    	edge2 = Part.makeLine(Pnt2,Pnt3)
    	edge3 = Part.makeLine(Pnt3,Pnt4)
    	edge4 = Part.makeLine(Pnt4,Pnt5)
    	edge5 = Part.makeLine(Pnt5,Pnt6)
    	edge6 = Part.makeLine(Pnt6,Pnt7)
    	edge7 = Part.Arc(Pnt7,Pnt8,Pnt9).toShape()

    	# create cutting tool for hexagon head
    	# Parameters s, k, outer circle diameter =  e/2.0+10.0
    	#extrude = self.makeHextool(s, k, s*2.0)

    	extrude = screw_maker2_2.Screw.makeHextool(o, s, k, s*2.0)

    	#if self.RealThread.isChecked():
    	if o.rThread:
		Pnt11 = Base.Vector(0.0,0.0,-r)        # helper point for real thread
      		edgeZ1 = Part.makeLine(Pnt9,Pnt11)
      		edgeZ0 = Part.makeLine(Pnt11,Pnt0)
      		aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7, \
          		edgeZ1, edgeZ0])

      		aFace =Part.Face(aWire)
      		head = aFace.revolve(Base.Vector(0.0,0.0,0.0),Base.Vector(0.0,0.0,1.0),360.0)
      		#FreeCAD.Console.PrintMessage("der Kopf mit revolve: " + str(dia) + "\n")

      		# Part.show(extrude)
      		head = head.cut(extrude)
      		#FreeCAD.Console.PrintMessage("der Kopf geschnitten: " + str(dia) + "\n")
      		#Part.show(head)

      		headFaces = []
      		for i in range(18):
        		headFaces.append(head.Faces[i])

      		if (dia < 3.0) or (dia > 5.0):
        		rthread = o.makeShellthread(dia, P, halfturns, True, offSet)
        		rthread.translate(Base.Vector(0.0, 0.0,-a-2.0*P))
        		#rthread.translate(Base.Vector(0.0, 0.0,-2.0*P))
        		#Part.show(rthread)
        		for tFace in rthread.Faces:
          			headFaces.append(tFace)
        		headShell = Part.Shell(headFaces)
        		head = Part.Solid(headShell)
      		else:
        		rthread = o.makeShellthread(dia, P, halfturns, False, offSet)
        		rthread.translate(Base.Vector(0.0, 0.0,-a-2.0*P))
        		#rthread.translate(Base.Vector(0.0, 0.0,-2.0*P))
        		#Part.show(rthread)
        		for tFace in rthread.Faces:
          			headFaces.append(tFace)
        		headShell = Part.Shell(headFaces)
        		head = Part.Solid(headShell)
        		cyl = o.cutChamfer(dia, P, l)
        		#FreeCAD.Console.PrintMessage("vor Schnitt Ende: " + str(dia) + "\n")
        		head = head.cut(cyl)

    	else:
      		# bolt points
      		cham_t = P*math.sqrt(3.0)/2.0*17.0/24.0

      		PntB0 = Base.Vector(0.0,0.0,-a)
      		PntB1 = Base.Vector(dia/2.0,0.0,-l+cham_t)
      		PntB2 = Base.Vector(dia/2.0-cham_t,0.0,-l)
      		PntB3 = Base.Vector(0.0,0.0,-l)

      		edgeB1 = Part.makeLine(Pnt10,PntB1)
      		edgeB2 = Part.makeLine(PntB1,PntB2)
      		edgeB3 = Part.makeLine(PntB2,PntB3)

      		edgeZ0 = Part.makeLine(PntB3,Pnt0)
      		if a <= r:
        		edgeB1 = Part.makeLine(Pnt9,PntB1)
        		aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7, \
            			edgeB1, edgeB2, edgeB3, edgeZ0])

      		else:
        		edge8 = Part.makeLine(Pnt9,Pnt10)
        		edgeB1 = Part.makeLine(Pnt10,PntB1)
        		aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8, \
            			edgeB1, edgeB2, edgeB3, edgeZ0])

      		aFace =Part.Face(aWire)
      		head = aFace.revolve(Base.Vector(0.0,0.0,0.0),Base.Vector(0.0,0.0,1.0),360.0)
      		#FreeCAD.Console.PrintMessage("der Kopf mit revolve: " + str(dia) + "\n")

      		# Part.show(extrude)
      		head = head.cut(extrude)
      		#FreeCAD.Console.PrintMessage("der Kopf geschnitten: " + str(dia) + "\n")

	fp.Shape = head # Part.Solid(head)

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

    def getIcon(self):
        __dirname__ = os.path.dirname(__file__)
        return(os.path.join(__dirname__, "icons", "createscrew.svg"))

