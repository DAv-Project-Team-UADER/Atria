# Copyright (C) 2026 El Equipo del Proyecto Atria
# Universidad Autónoma de Entre Ríos (UADER FCYT, sede Concepción del Uruguay)
# Bajo la dirección de Ernesto Ledesma
# Encargados: Micaela Saül, Tadeo Rochas y Camila Viñeg
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.

import FreeCAD as App
import FreeCADGui as Gui

class ObjectSelection:
    def __init__(self):
        # Internal list of object names to iterate through
        self._ObjectNames = []
        # Current index inside the list
        self._CurrentIndex = 0
        # Index of the last actually selected object
        self._LastSelectedIndex = -1
        # Internal state of the boolean property
        self._SelectOther = False

    def MonoSelection(self, Obj):
        """Highlights a specific object and focuses it in the 3D view and the tree."""
        if not Obj:
            print("Error: The provided object is not valid.")
            return
            
        Gui.Selection.clearSelection()           # Clears previous selections
        Gui.Selection.addSelection(Obj)          # Makes the object glow (3D and Tree)
        try:
            Gui.Control.showInTree()                 # Focuses and scrolls the tree view to it
        except AttributeError:
            pass # Not available in FreeCAD 1.1+
        Gui.SendMsgToActiveView("ViewSelection") # Centers the 3D camera onto the object
        print(f"Successfully focused: '{Obj.Name}'")

    def VectorSelection(self, ListNames):
        """Initializes the list of object names and resets the counter."""
        if not isinstance(ListNames, list):
            print("Error: A list or vector of strings containing the names is required.")
            return
            
        self._ObjectNames = ListNames
        self._CurrentIndex = 0
        self._LastSelectedIndex = -1
        print(f"List loaded with {len(self._ObjectNames)} objects. Ready to iterate.")

    @property
    def SelectOther(self):
        """Allows reading the current state of the property."""
        return self._SelectOther

    def SelectNext(self):
        """Advances to the next object in the list (cyclic).

        If the list is empty, loads all objects from the active document first.
        """
        ActiveDoc = App.activeDocument()

        if not ActiveDoc:
            print("Error: There is no active document in FreeCAD.")
            return

        if not self._ObjectNames:
            ObjectNames = [Obj.Name for Obj in ActiveDoc.Objects]
            self.VectorSelection(ObjectNames)

        if not self._ObjectNames:
            print("Error: The document has no objects.")
            return

        CurrentName = self._ObjectNames[self._CurrentIndex]
        Obj = ActiveDoc.getObject(CurrentName)

        if Obj:
            print(f"\n[Next] Object {self._CurrentIndex + 1} of {len(self._ObjectNames)}")
            self.MonoSelection(Obj)
        else:
            print(f"Warning: The object '{CurrentName}' does not exist in the current document.")

        self._LastSelectedIndex = self._CurrentIndex
        self._CurrentIndex = (self._CurrentIndex + 1) % len(self._ObjectNames)

    def SelectPrevious(self):
        """Goes back to the previous object in the list (cyclic).

        If the list is empty, loads all objects from the active document first.
        """
        ActiveDoc = App.activeDocument()

        if not ActiveDoc:
            print("Error: There is no active document in FreeCAD.")
            return

        if not self._ObjectNames:
            ObjectNames = [Obj.Name for Obj in ActiveDoc.Objects]
            self.VectorSelection(ObjectNames)

        if not self._ObjectNames:
            print("Error: The document has no objects.")
            return

        if self._LastSelectedIndex >= 0:
            target = (self._LastSelectedIndex - 1) % len(self._ObjectNames)
        else:
            target = (self._CurrentIndex - 1) % len(self._ObjectNames)

        CurrentName = self._ObjectNames[target]
        Obj = ActiveDoc.getObject(CurrentName)

        if Obj:
            print(f"\n[Previous] Object {target + 1} of {len(self._ObjectNames)}")
            self.MonoSelection(Obj)
        else:
            print(f"Warning: The object '{CurrentName}' does not exist in the current document.")

        self._LastSelectedIndex = target
        self._CurrentIndex = (target + 1) % len(self._ObjectNames)

    def SelectAll(self):
        """Selects all objects in the active document."""
        ActiveDoc = App.activeDocument()

        if not ActiveDoc:
            print("Error: There is no active document in FreeCAD.")
            return

        Gui.Selection.clearSelection()

        for Obj in ActiveDoc.Objects:
            Gui.Selection.addSelection(Obj)

        print(f"Selected {len(ActiveDoc.Objects)} objects.")

    def DeselectAll(self):
        """Clears the current selection."""
        Gui.Selection.clearSelection()
        print("Selection cleared.")

    def DeleteSelected(self):
        """Deletes the currently selected object.

        Uses the internal _LastSelectedIndex when available (set by
        SelectNext/SelectPrevious); otherwise falls back to the
        current Gui selection. Keeps the internal name list in sync
        and recomputes the document.
        """
        ActiveDoc = App.activeDocument()

        if not ActiveDoc:
            print("Error: There is no active document in FreeCAD.")
            return

        # 1) Preferred: object tracked by SelectNext/Previous
        Name = self.GetCurrentObject()
        if Name:
            Obj = ActiveDoc.getObject(Name)
            if not Obj:
                print(f"Warning: The object '{Name}' does not exist in the current document.")
                return
            try:
                ActiveDoc.removeObject(Name)
                ActiveDoc.recompute()
                print(f"Deleted object: '{Name}'")
            except Exception as exc:
                print(f"Error deleting '{Name}': {exc}")
                return
            # Keep internal list consistent
            try:
                idx = self._ObjectNames.index(Name)
                self._ObjectNames.pop(idx)
            except ValueError:
                idx = self._LastSelectedIndex
            if not self._ObjectNames:
                self._CurrentIndex = 0
                self._LastSelectedIndex = -1
                print("No more objects in list.")
            else:
                # After removal the next object occupies the same index
                if idx >= len(self._ObjectNames):
                    idx = 0
                self._LastSelectedIndex = -1
                # Point _CurrentIndex so that next SelectNext picks idx
                self._CurrentIndex = idx
            try:
                Gui.Selection.clearSelection()
            except Exception:
                pass
            return

        # 2) Fallback: whatever is selected in the GUI
        try:
            GuiSelected = Gui.Selection.getSelection()
        except Exception:
            GuiSelected = []
        if GuiSelected:
            Deleted = []
            for Obj in list(GuiSelected):
                ObjName = getattr(Obj, "Name", None)
                if not ObjName:
                    continue
                try:
                    ActiveDoc.removeObject(ObjName)
                    Deleted.append(ObjName)
                except Exception as exc:
                    print(f"Error deleting '{ObjName}': {exc}")
                if ObjName in self._ObjectNames:
                    try:
                        self._ObjectNames.remove(ObjName)
                    except ValueError:
                        pass
            if Deleted:
                try:
                    ActiveDoc.recompute()
                except Exception:
                    pass
                print(f"Deleted object(s): {', '.join(Deleted)}")
                self._LastSelectedIndex = -1
                self._CurrentIndex = 0
                try:
                    Gui.Selection.clearSelection()
                except Exception:
                    pass
                if not self._ObjectNames:
                    print("No more objects in list.")
            return

        print("No object selected. Say 'avanzar' or 'anterior' to select one, then 'borrar'.")

    def GetCurrentObject(self):
        """Returns the name of the last selected object, or None."""
        if not self._ObjectNames or self._LastSelectedIndex < 0:
            return None

        return self._ObjectNames[self._LastSelectedIndex]

    def GetObjectCount(self):
        """Returns the number of objects in the current list."""
        return len(self._ObjectNames)

    @SelectOther.setter
    def SelectOther(self, Value):
        """Triggers automatically when the user writes 'Instance.SelectOther = True'."""
        if Value is True:
            self.SelectNext()
        else:
            self._SelectOther = Value
