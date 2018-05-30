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

import os
import FreeCAD
import FreeCADGui as Gui

from .features import ViewProviderConstructionToy, plate, separator, washer, screw


class BaseCommand(object):
    def __init__(self):
        pass

    def IsActive(self):
        if FreeCAD.ActiveDocument is None:
            return False
        else:
            return True

class CreatePlate(BaseCommand):
    """creates a construction plate"""

    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(__file__),  'icons', 'createplate.svg'), 
                'MenuText': 'create plate', 
                'ToolTip': 'create plate'}

    def Activated(self):
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Plate")
        plate(a)
        ViewProviderConstructionToy(a.ViewObject)
        FreeCAD.ActiveDocument.recompute()
        Gui.SendMsgToActiveView("ViewFit")


class CreateSeparator(BaseCommand):
    """creates a construction separator"""

    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(__file__),  'icons', 'createseparator.svg'), 
                'MenuText': 'create separator', 
                'ToolTip': 'create separator'}  

    def Activated(self):
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Separator")
        separator(a)
        ViewProviderConstructionToy(a.ViewObject)
        FreeCAD.ActiveDocument.recompute()
        Gui.SendMsgToActiveView("ViewFit")

class CreateWasher(BaseCommand):
    """creates a construction washer"""

    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(__file__),  'icons', 'createwasher.svg'), 
                'MenuText': 'create washer', 
                'ToolTip': 'create washer'}  

    def Activated(self):
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Washer")
        washer(a)
        ViewProviderConstructionToy(a.ViewObject)
        FreeCAD.ActiveDocument.recompute()
        Gui.SendMsgToActiveView("ViewFit")

class CreateScrew(BaseCommand):
    """creates a construction screw"""

    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(__file__),  'icons', 'createscrew.svg'), 
                'MenuText': 'create screw', 
                'ToolTip': 'create screw'}  

    def Activated(self):
        a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Screw")
        screw(a)
        ViewProviderConstructionToy(a.ViewObject)
        FreeCAD.ActiveDocument.recompute()
        Gui.SendMsgToActiveView("ViewFit")
