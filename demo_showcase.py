"""Extra voice commands for the 2D and 3D showcase."""

NAMES = [
    ('Casa2D', 'Casa 2D', ('casa dos de', 'fachada', 'casa dos d')),
    ('Prueba3D', 'Prueba 3D', ('prueba tres de', 'prueba tres d', 'prueba de arquitectura')),
    ('Casa3D', 'Casa 3D', ('casa tres de', 'casa tres d')),
]

WALLS = [
    ('Izquierda', 'Frente', ('frente', 'pared del frente', 'delante', 'frontal')),
    ('CostadoDerecho', 'Costado derecho', ('derecha', 'costado derecho', 'pared derecha', 'lateral derecho')),
    ('CostadoIzquierdo', 'Costado izquierdo', ('izquierda', 'costado izquierdo', 'pared izquierda', 'lateral izquierdo')),
    ('Fondo', 'Fondo', ('fondo', 'pared del fondo', 'trasera', 'pared trasera')),
]

SQUARE = ('crear cuadrado', 'dibujar cuadrado', 'hacer un cuadrado', 'dibujar un cuadrado', 'crear un cuadrado')
DOOR_2D = ('crear puerta dos de', 'dibujar puerta', 'dibujar una puerta', 'crear rectangulo para puerta')
WINDOWS_2D = ('agregar ventanas al dibujo', 'anadir ventanas al dibujo', 'dibujar ventanas')
ROOF_2D = ('dibujar techo a dos aguas', 'agregar techo al dibujo', 'anadir techo al dibujo')
WINDOWS_SHORT = ('poner ventanas', 'colocar ventanas', 'insertar ventanas', 'agregar ventanas', 'anadir ventanas')
ROOF_SHORT = ('poner techo a dos aguas', 'colocar techo a dos aguas', 'insertar techo a dos aguas',
              'agregar techo a dos aguas', 'anadir techo a dos aguas')
FINISH_2D = ('completar fachada', 'terminar fachada', 'completar casa dos de', 'terminar casa dos de')
NAME_COMMANDS = ('nuevo archivo con nombre', 'crear archivo con nombre', 'nuevo documento con nombre')
WINDOW_3D = ('colocar ventana', 'colocar una ventana', 'poner ventana', 'poner una ventana',
             'insertar ventana', 'insertar una ventana', 'agregar ventana', 'agregar una ventana',
             'anadir ventana', 'anadir una ventana')


class Showcase:
    def __init__(self, demo, measure):
        self.demo = demo
        self.measure = measure

    @staticmethod
    def phrases():
        phrases = [*SQUARE, *DOOR_2D, *WINDOWS_2D, *ROOF_2D, *WINDOWS_SHORT, *ROOF_SHORT,
                   *FINISH_2D, *NAME_COMMANDS, *WINDOW_3D]
        phrases += [alias for _, _, aliases in (*NAMES, *WALLS) for alias in aliases]
        phrases += [phrase.replace('anadir', 'añadir').replace('rectangulo', 'rectángulo') for phrase in phrases]
        return phrases

    def handle(self, phrase):
        if phrase in NAME_COMMANDS:
            return self.demo.ask_choice('document_name', 'Elegí el nombre. Decí «Casa dos de», «Prueba tres de» o «Casa tres de».', NAMES, self.new_document)
        if phrase in SQUARE:
            return self.square()
        if phrase in DOOR_2D:
            return self.door()
        if phrase in (*WINDOWS_2D, *ROOF_2D, *FINISH_2D):
            return self.finish(phrase)
        if phrase in (*WINDOWS_SHORT, *ROOF_SHORT) and self.active_facade():
            return self.finish(WINDOWS_2D[0] if phrase in WINDOWS_SHORT else ROOF_2D[0])
        if phrase in WINDOW_3D:
            return self.window_choice()
        return None

    def new_document(self, key):
        import FreeCAD as App
        label = next(label for name, label, _aliases in NAMES if name == key)
        App.newDocument(key, label)
        self.demo.pending = None
        self.demo.tell(f'Documento creado: {label}.')

    def bounded_measure(self, text, minimum, maximum):
        value = self.measure(text, 'mm')
        if not minimum <= value <= maximum:
            raise ValueError(f'La medida debe estar entre {minimum:g} y {maximum:g} mm.')
        return value

    def square(self):
        import FreeCAD as App
        doc = App.ActiveDocument or App.newDocument('Casa2D', 'Casa 2D')
        if doc.getObject('Demo2DCuerpo') or doc.getObject('CasaPiso'):
            raise ValueError('Para iniciar otro dibujo, decí «nuevo archivo con nombre».')

        def create(side):
            self.require_active(doc)
            self.shape(doc, 'Demo2DCuerpo', 'Cuadrado de la fachada',
                       [(0, 0), (side, 0), (side, side), (0, side)], face=False)
            self.done(doc, 'Cuadrado listo. Decí «dibujar puerta».')

        return self.demo.ask('square_side', '¿Cuánto mide el lado del cuadrado? Ejemplo: cuatro mil milímetros.',
                             parse=lambda text: self.bounded_measure(text, 1000, 12000), on_accept=create)

    def door(self):
        doc, side = self.facade()
        if doc.getObject('Demo2DPuerta'):
            return self.demo.tell('El dibujo ya tiene puerta.')

        def ask_height(width):
            def create(height):
                self.require_active(doc)
                self.add_door(doc, side, width, height)
                self.done(doc, 'Puerta dibujada. Decí «completar fachada» para agregar ventanas y techo.')

            return self.demo.ask('door2d_height', '¿Qué altura tiene el rectángulo de la puerta? Ejemplo: dos mil cien milímetros.',
                                 parse=lambda text: self.bounded_measure(text, side * .10, side * .8), on_accept=create)

        return self.demo.ask('door2d_width', '¿Qué ancho tiene el rectángulo de la puerta? Ejemplo: novecientos milímetros.',
                             parse=lambda text: self.bounded_measure(text, side * .10, side * .32), on_accept=ask_height)

    def finish(self, phrase):
        doc, side = self.facade()
        doc.openTransaction('Completar fachada 2D')
        try:
            if phrase in FINISH_2D and not doc.getObject('Demo2DPuerta'):
                self.add_door(doc, side, side * .225, side * .525)
            if phrase in (*WINDOWS_2D, *FINISH_2D):
                for name, center in [('Izquierda', .23), ('Derecha', .77)]:
                    if not doc.getObject('Demo2DVentana'+name):
                        self.add_window(doc, side, name, center)
            if phrase in (*ROOF_2D, *FINISH_2D) and not doc.getObject('Demo2DTecho'):
                self.shape(doc, 'Demo2DTecho', 'Techo a dos aguas en alzado',
                           [(-side*.08, side), (side*1.08, side), (side/2, side*1.35)], (.66, .20, .13))
            doc.recompute()
            doc.commitTransaction()
        except Exception:
            doc.abortTransaction()
            raise
        return self.done(doc, 'Fachada actualizada.')

    def add_door(self, doc, side, width, height):
        x = (side - width) / 2
        self.shape(doc, 'Demo2DPuerta', 'Puerta rectangular',
                   [(x, 0), (x+width, 0), (x+width, height), (x, height)], (.58, .32, .14))

    def add_window(self, doc, side, name, center):
        x, y = side * (center - .095), side * .35
        size = side * .19
        self.shape(doc, 'Demo2DVentana'+name, 'Ventana '+name.lower(),
                   [(x,y), (x+size,y), (x+size,y+size), (x,y+size)], (.43, .70, .89))
        self.shape(doc, 'Demo2DTravesano'+name, 'Travesaño '+name.lower(),
                   [(x,y+size/2), (x+size,y+size/2)], face=False)

    @staticmethod
    def shape(doc, name, label, points, color=None, face=True):
        import FreeCAD as App
        import Part
        vertices = [App.Vector(x, y, 0) for x, y in points]
        wire = Part.makePolygon(vertices + vertices[:1] if len(vertices) > 2 else vertices)
        obj = doc.addObject('Part::Feature', name)
        obj.Label = label
        obj.Shape = Part.Face(wire) if face else wire
        obj.ViewObject.LineColor = (.18, .19, .21)
        obj.ViewObject.LineWidth = 3
        if color:
            obj.ViewObject.ShapeColor = color
        return obj

    @staticmethod
    def require_active(doc):
        import FreeCAD as App
        if App.ActiveDocument != doc:
            raise ValueError('Volvé al documento en el que empezaste este paso.')

    @staticmethod
    def active_facade():
        import FreeCAD as App
        doc = App.ActiveDocument
        return doc if doc and doc.getObject('Demo2DCuerpo') and not doc.getObject('CasaPiso') else None

    def facade(self):
        doc = self.active_facade()
        body = doc.getObject('Demo2DCuerpo') if doc else None
        if body is None:
            raise ValueError('Primero decí «crear cuadrado».')
        return doc, body.Shape.BoundBox.XLength

    def done(self, doc, message):
        import FreeCADGui as Gui
        self.demo.pending = None
        doc.recompute()
        view = Gui.activeDocument().activeView()
        view.viewTop()
        view.fitAll()
        return self.demo.tell(message)

    def window_choice(self):
        import FreeCAD as App
        active = App.ActiveDocument
        if not active or not active.getObject('CasaPiso'):
            return None  # Keep the standard Architecture command outside a demo house.
        doc, floor = self.demo.current()
        if not doc.getObject('CasaFrente'):
            raise ValueError('Primero decí «rodear piso de paredes».')

        def place(position):
            self.require_active(doc)
            if position == 'Izquierda' and doc.getObject('CasaVentanaIzquierda'):
                position = 'Derecha'
            self.demo.pending = None
            if doc.getObject('CasaVentana'+position):
                return self.demo.tell('Esa pared ya tiene su ventana de la demo.')
            self.demo.mutate(doc, 'Ventana', lambda: self.demo.windows(doc, floor, [position]))
            return self.demo.tell('Ventana colocada con vidrio y abertura en el muro elegido.')

        return self.demo.ask_choice('window_wall', '¿En qué pared? Decí «frente», «costado derecho», «costado izquierdo» o «fondo».', WALLS, place)

    def move_selection(self):
        import FreeCAD as App
        import FreeCADGui as Gui

        doc = App.ActiveDocument
        if not doc or not doc.getObject('CasaPiso'):
            return None
        selection = tuple(obj.Name for obj in Gui.Selection.getSelection())
        if not selection:
            raise ValueError('Seleccioná al menos un objeto para mover.')

        from InputPrompts.SpokenNumberParser import SpokenNumberParser
        from Modify.commands import move

        def ask_axis(index, offsets):
            self.require_active(doc)
            if tuple(obj.Name for obj in Gui.Selection.getSelection()) != selection:
                raise ValueError('La selección cambió. Volvé a iniciar el movimiento.')
            if index == 3:
                move(vector=offsets)
                return self.demo.tell('Desplazamiento aplicado.')
            axis = 'XYZ'[index]
            return self.demo.ask(
                'move_' + axis.lower(), f'¿Cuántos milímetros querés mover en {axis}?',
                parse=SpokenNumberParser.ParseFloat,
                on_accept=lambda value: ask_axis(index + 1, (*offsets, value)),
            )

        return ask_axis(0, ())
