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
import FreeCADGui as Gui
import FreeCAD as App
__dirname__ = os.path.dirname(__file__)

try:
    from FreeCADGui import Workbench
except ImportError as e:
    App.Console.PrintWarning("you are using an old version of FreeCAD")

class constructionToyWorkbench(Workbench):
    """construction toy workbench"""
    MenuText = "Construction Toy"
    ToolTip = "Construction Toy Workbench"
    Icon = os.path.join(__dirname__,  'icons', 'constructiontoyworkbench.svg')
    commands = [
                "CreatePlate"]

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
	# imports
        from .commands import CreatePlate
        self.appendToolbar("Construction Toy", self.commands)
        self.appendMenu("Construction Toy", self.commands)
        Gui.addIconPath(App.getHomePath()+"Mod/constructiontoy/icons/")
        Gui.addCommand('CreatePlate', CreatePlate())

    def Activated(self):
        pass


    def Deactivated(self):
        pass

Gui.addWorkbench(constructionToyWorkbench())
