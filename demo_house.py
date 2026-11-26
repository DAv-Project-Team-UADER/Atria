"""Local, voice-driven house demonstration. Dimensions are stored in millimetres.

No changes to the upstream BIM commands. All CAD work runs on the GUI thread
through BrowserVoiceAdapter. Questions are non-modal and answered by voice.
"""
from __future__ import annotations

import math
import re
import unicodedata
from pathlib import Path

COMMANDS = {
    'rodear piso de paredes': 'walls', 'rodear el piso de paredes': 'walls',
    'rodear piso con paredes': 'walls', 'levantar paredes': 'walls',
    'poner puerta al frente': 'door', 'colocar puerta': 'door',
    'poner una ventana al frente': 'front_window', 'poner ventana al frente': 'front_window',
    'poner una ventana al costado': 'side_window', 'poner ventana al costado': 'side_window',
    'poner ventana al costado derecho': 'side_window',
    'poner dos ventanas al frente': 'windows', 'poner dos ventanas': 'windows',
    'colocar ventanas': 'windows',
    'poner techo a dos aguas': 'roof', 'crear techo a dos aguas': 'roof',
    'construir techo': 'roof',
    'ocultar techo': 'hide', 'mostrar techo': 'show',
    'ver casa': 'view', 'guardar casa': 'save',
    'ayuda casa': 'help', 'cancelar casa': 'cancel',
}
for verb in ('poner', 'colocar', 'insertar', 'agregar', 'añadir'):
    for object_phrase, action in {
        'puerta al frente': 'door', 'una puerta al frente': 'door',
        'ventana al frente': 'front_window', 'una ventana al frente': 'front_window',
        'ventana al costado': 'side_window', 'una ventana al costado': 'side_window',
        'ventana al costado derecho': 'side_window',
        'dos ventanas al frente': 'windows', 'techo a dos aguas': 'roof',
    }.items():
        COMMANDS[f'{verb} {object_phrase}'.replace('ñ', 'n')] = action

CONFIRMATIONS = {'aceptar', 'enviar', 'confirmar', 'listo', 'ok', 'okey'}
NUMBERS = dict(zip('cero uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciseis diecisiete dieciocho diecinueve veinte veintiuno veintidos veintitres veinticuatro veinticinco veintiseis veintisiete veintiocho veintinueve'.split(), range(30)))
NUMBERS.update({'un': 1, 'una': 1, 'treinta': 30, 'cuarenta': 40, 'cincuenta': 50, 'sesenta': 60, 'setenta': 70, 'ochenta': 80, 'noventa': 90, 'cien': 100, 'ciento': 100, 'doscientos': 200, 'trescientos': 300, 'cuatrocientos': 400, 'quinientos': 500, 'seiscientos': 600, 'setecientos': 700, 'ochocientos': 800, 'novecientos': 900})


def normalize(text):
    text = ''.join(c for c in unicodedata.normalize('NFKD', text.lower()) if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', text).strip().removesuffix(' enviar').strip()


def number(text):
    text = text.strip().replace(',', '.')
    if re.fullmatch(r'\d+(?:\.\d+)?', text):
        return float(text)
    parts = re.split(r'\s+(?:coma|punto)\s+', text)
    if len(parts) > 2:
        raise ValueError('Deci una sola medida, por ejemplo dos coma seis metros.')
    total = 0
    for word in parts[0].split():
        if word == 'y':
            continue
        if word == 'mil':
            total = (total or 1) * 1000
        elif word in NUMBERS:
            total += NUMBERS[word]
        else:
            raise ValueError('No entendi la medida. Ejemplo: quince centimetros.')
    if not parts[0]:
        raise ValueError('Falta la medida.')
    if len(parts) == 2:
        words = parts[1].split()
        if all(w in NUMBERS and NUMBERS[w] < 10 for w in words) and words:
            fraction = ''.join(str(NUMBERS[w]) for w in words)
        elif re.fullmatch(r'\d+', parts[1]):
            fraction = parts[1]
        else:
            fraction = str(int(number(parts[1])))
        total += float('0.' + fraction)
    return float(total)


def measure(text, default_unit):
    text = normalize(text)
    match = re.search(r'\s*(milimetros?|centimetros?|metros?|mm|cm|m)$', text)
    unit = default_unit
    if match:
        word = match.group(1)
        unit = 'mm' if word.startswith('mili') or word == 'mm' else 'cm' if word.startswith('cent') or word == 'cm' else 'm'
        text = text[:match.start()].strip()
    value = number(text) * {'m': 1000, 'cm': 10, 'mm': 1}[unit]
    if not math.isfinite(value) or value <= 0:
        raise ValueError('La medida debe ser mayor que cero.')
    return value


class HouseDemo:
    def __init__(self, ui=True, refresh_grammar=None):
        from demo_showcase import Showcase

        self.pending = None
        self.values = {}
        self.ui = ui
        self.label = None
        self.question = ''
        self.prompt = None
        self.choice_words = None
        self.refresh_grammar = refresh_grammar or (lambda: None)
        self.showcase = Showcase(self, measure)

    def tell(self, message):
        print('[CASA] ' + message)
        if self.ui:
            import FreeCADGui as Gui
            from PySide6 import QtCore, QtWidgets as QtGui
            if self.label is None:
                dock = QtGui.QDockWidget('Demo casa por voz', Gui.getMainWindow())
                dock.setObjectName('AtriaHouseDemo')
                self.label = QtGui.QLabel()
                self.label.setWordWrap(True)
                self.label.setMinimumWidth(260)
                self.label.setStyleSheet('padding: 12px; font-size: 15px;')
                dock.setWidget(self.label)
                Gui.getMainWindow().addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
            self.label.setText(message)
            self.label.parentWidget().show()
        return message

    def grammar(self):
        phrases = ['crear piso', 'iniciar casa', 'cancelar casa', 'cancelar', 'ayuda casa']
        # Numeric words also allow dimensions such as cuatro coma cinco por seis.
        phrases += list(NUMBERS) + ['mil', 'menos', 'y', 'por', 'de', 'metros', 'metro', 'centimetros', 'centimetro', 'milimetros', 'milimetro', 'coma', 'punto', 'enviar']
        phrases += ['crear piso de cuatro por cuatro', 'crear piso de cinco por cuatro', 'dos coma seis metros', 'quince centimetros', 'veinte centimetros']
        phrases.extend(COMMANDS)
        phrases.extend(phrase.replace('anadir ', 'añadir ', 1) for phrase in COMMANDS if phrase.startswith('anadir '))
        phrases.extend(('centímetro', 'centímetros', 'milímetro', 'milímetros'))
        phrases.extend(CONFIRMATIONS)
        phrases.extend(self.showcase.phrases())
        return phrases

    def ask(self, stage, question, *, parse=None, on_accept=None):
        parser = parse or (lambda text: self.parse_measure(stage, text))
        if not self.ui:
            self.pending = stage
            self.question = question
            return self.tell(question)

        import FreeCADGui as Gui
        from InputPrompts.FloatInputPrompt import FloatInputPrompt

        class HouseMeasurePrompt(FloatInputPrompt):
            def _ParseAccumulatedText(self, text):
                return parser(text)

        prompt = HouseMeasurePrompt('ATRIA — Medida de la casa', question + '\nDictá el valor y decí «aceptar».', Gui.getMainWindow())
        return self.show_prompt(stage, question, prompt, on_accept or self.answer)

    def ask_options(self, stage, question, aliases, on_accept, labels=None):
        options = {}
        for phrase, key in aliases.items():
            options.setdefault(key, []).append(phrase)
        choices = [
            (key, labels[key] if labels else words[0].capitalize(), words)
            for key, words in options.items()
        ]
        return self.ask_choice(stage, question, choices, on_accept)

    def ask_choice(self, stage, question, options, on_accept):
        import FreeCADGui as Gui
        from InputPrompts.ChoiceInputPrompt import ChoiceInputPrompt

        class DemoChoicePrompt(ChoiceInputPrompt):
            def _OnOkClicked(self):
                self.AcceptValue(self.GetSelectedKey())

            def ProcessFinalText(self, text):
                words = normalize(text).split()
                if words and words[-1] in CONFIRMATIONS:
                    words.pop()
                phrase = ' '.join(words)
                for key, _, aliases in options:
                    if phrase in aliases:
                        self.SetHeardText(text)
                        return self.AcceptValue(key)
                return super().ProcessFinalText(text)

        options = [(key, label, tuple(normalize(word) for word in aliases))
                   for key, label, aliases in options]
        prompt = DemoChoicePrompt(options, 'ATRIA — Elegir en la demo', question, Gui.getMainWindow())
        words = {word for _, _, aliases in options for word in aliases}
        return self.show_prompt(stage, question, prompt, on_accept, words | {'arriba', 'abajo'})

    def show_prompt(self, stage, question, prompt, on_accept, choice_words=None):
        from PySide6.QtCore import Qt

        self.close_prompt()
        self.pending = stage
        self.question = question
        self.choice_words = choice_words
        prompt.setWindowModality(Qt.WindowModality.NonModal)
        self.prompt = prompt

        def finish(_result):
            if self.prompt is not prompt:
                return
            self.prompt = None
            self.choice_words = None
            result = prompt.GetResult()
            prompt.deleteLater()
            if result.Success:
                try:
                    on_accept(result.Value)
                    if self.prompt is None:
                        self.pending = None
                except Exception as exc:
                    self.pending = None
                    self.tell(f'No se pudo completar el paso. {exc}')
            else:
                self.cancel_question()
            self.refresh_grammar()

        prompt.finished.connect(finish)
        prompt.Show()
        self.refresh_grammar()
        print('[CASA] ' + question)
        return question

    def close_prompt(self):
        prompt, self.prompt = self.prompt, None
        self.choice_words = None
        if prompt is not None:
            prompt.reject()
            prompt.deleteLater()

    def cancel_question(self):
        self.close_prompt()
        self.pending = None
        self.values = {}
        self.refresh_grammar()
        return self.tell('Pregunta cancelada. La casa no se borro.')

    @staticmethod
    def is_measure_phrase(phrase):
        first_word = phrase.partition(' ')[0]
        return first_word in NUMBERS or first_word in ('mil', 'menos') or bool(re.match(r'^\d', first_word))

    def uses_raw_phrase(self, phrase):
        if self.prompt is None:
            return False
        if self.choice_words is None:
            return phrase in CONFIRMATIONS or self.is_measure_phrase(phrase)
        words = phrase.split()
        if words and words[-1] in CONFIRMATIONS:
            words.pop()
        return phrase in CONFIRMATIONS or ' '.join(words) in self.choice_words

    def handle(self, phrase):
        if self.uses_raw_phrase(phrase):
            self.prompt.ProcessFinalText(phrase)
            return 'Medida recibida.'
        phrase = normalize(phrase)
        if phrase in ('cancelar casa', 'cancelar'):
            if not self.pending and phrase == 'cancelar':
                return None
            return self.cancel_question()
        showcase_result = self.showcase.handle(phrase)
        if showcase_result is not None:
            return showcase_result
        if phrase == 'ayuda casa':
            help_text = 'Crear piso de cuatro por cuatro → espesor. Rodear piso de paredes → altura → espesor. Poner puerta al frente. Poner una ventana al frente. Poner una ventana al costado. Poner dos ventanas al frente. Poner techo a dos aguas. Ocultar techo. Mostrar techo. Guardar casa.'
            return self.tell(help_text + ('\n' + self.question if self.pending else ''))
        if phrase in ('crear piso', 'iniciar casa'):
            self.values = {}
            return self.ask('length', '¿Cuanto mide el frente del piso? Deci, por ejemplo, cuatro metros.')
        if phrase.startswith('crear piso de '):
            dimensions = re.split(r'\s+por\s+|\s*x\s*', phrase[len('crear piso de '):])
            if len(dimensions) != 2:
                raise ValueError('Deci crear piso de cuatro por cuatro, o solamente crear piso.')
            length, width = [measure(p, 'm') for p in dimensions]
            self.check_size(length, width)
            self.values = {'length': length, 'width': width}
            return self.ask('floor_thickness', f'Piso de {length/1000:g} por {width/1000:g} metros. ¿Que espesor? Por ejemplo quince centimetros.')
        command = COMMANDS.get(phrase)
        if command is None:
            if self.pending and self.is_measure_phrase(phrase):
                return self.answer(self.parse_measure(self.pending, phrase))
            return None
        doc, floor = self.current()
        if command == 'walls':
            if doc.getObject('CasaFrente'):
                return self.tell('Las paredes ya estan creadas.')
            self.values = {'document': doc.Name}
            return self.ask('height', '¿Que altura tienen las paredes? Por ejemplo dos coma seis metros.')
        if command in ('door', 'windows', 'front_window', 'side_window', 'roof'):
            if not doc.getObject('CasaFrente'):
                raise ValueError('Primero deci rodear piso de paredes.')
            if command == 'door':
                if doc.getObject('CasaPuerta'):
                    return self.tell('La puerta ya esta puesta.')
                self.mutate(doc, 'Puerta', lambda: self.door(doc, floor))
                return self.tell('Puerta centrada al frente, con abertura real.')
            if command in ('windows', 'front_window', 'side_window'):
                positions = {
                    'windows': ('Izquierda', 'Derecha'),
                    'front_window': ('Izquierda',),
                    'side_window': ('CostadoDerecho',),
                }
                missing = [pos for pos in positions[command] if not doc.getObject('CasaVentana' + pos)]
                if not missing:
                    return self.tell('Ya estan colocadas las ventanas de ese comando.')
                self.mutate(doc, 'Ventanas', lambda: self.windows(doc, floor, missing))
                if command == 'side_window':
                    return self.tell('Ventana colocada en el costado derecho, con hueco y vidrio.')
                if command == 'front_window':
                    return self.tell('Ventana colocada a la izquierda del frente, con hueco y vidrio.')
                return self.tell('El frente tiene sus dos ventanas, con vidrio y huecos reales.')
            if doc.getObject('CasaTechoIzquierdo'):
                return self.tell('El techo ya esta creado. Podes decir mostrar techo.')
            self.mutate(doc, 'Techo', lambda: self.roof(doc, floor))
            return self.tell('Techo a dos aguas listo. Deci ocultar techo para mostrar el interior.')
        if command in ('show', 'hide'):
            if not doc.getObject('CasaTechoIzquierdo'):
                raise ValueError('Primero deci poner techo a dos aguas.')
            for name in ('CasaTechoIzquierdo', 'CasaTechoDerecho'):
                doc.getObject(name).ViewObject.Visibility = command == 'show'
            return self.tell('Techo visible.' if command == 'show' else 'Techo oculto.')
        if command == 'view':
            self.view()
            return self.tell('Casa encuadrada en vista isometrica.')
        if command == 'save':
            import os
            local_outputs = os.environ.get('ATRIA_DEMO_OUTPUTS')
            folder = Path(local_outputs) if local_outputs else Path.home() / 'ATRIA' / 'outputs'
            folder.mkdir(parents=True, exist_ok=True)
            target = folder / (doc.Name + '.FCStd')
            count = 2
            while target.exists():
                target = folder / f'{doc.Name}-{count}.FCStd'
                count += 1
            doc.recompute()
            doc.saveAs(str(target))
            return self.tell('Casa guardada en ' + str(target))

    @staticmethod
    def check_size(length, width):
        if not (3500 <= length <= 12000 and 3000 <= width <= 12000):
            raise ValueError('Para esta demo: frente entre 3,5 y 12 metros; fondo entre 3 y 12 metros.')

    def parse_measure(self, stage, phrase):
        value = measure(phrase, 'cm' if stage in ('floor_thickness', 'wall_thickness') else 'm')
        if stage == 'length':
            self.check_size(value, 4000)
        elif stage == 'width':
            self.check_size(self.values['length'], value)
        elif stage == 'floor_thickness' and not 50 <= value <= 500:
            raise ValueError('El espesor del piso debe estar entre 5 y 50 centimetros.')
        elif stage == 'height' and not 2400 <= value <= 4000:
            raise ValueError('Altura entre 2,4 y 4 metros. Ejemplo: dos coma seis metros.')
        elif stage == 'wall_thickness' and not 100 <= value <= 300:
            raise ValueError('Espesor de paredes entre 10 y 30 centimetros.')
        return value

    def answer(self, value):
        stage = self.pending
        if stage == 'length':
            self.values['length'] = value
            return self.ask('width', '¿Cuanto mide el fondo? Por ejemplo cuatro metros.')
        if stage == 'width':
            self.values['width'] = value
            return self.ask('floor_thickness', '¿Que espesor tiene el piso? Por ejemplo quince centimetros.')
        if stage == 'floor_thickness':
            self.floor(self.values['length'], self.values['width'], value)
            self.pending = None
            return self.tell('Piso listo. Deci rodear piso de paredes.')
        if stage == 'height':
            self.values['height'] = value
            return self.ask('wall_thickness', '¿Que espesor tienen las paredes? Por ejemplo veinte centimetros.')
        if stage == 'wall_thickness':
            doc, floor = self.current()
            if doc.Name != self.values['document']:
                raise ValueError('Volviste a otro documento. Regresa a la casa o deci cancelar casa.')
            if doc.getObject('CasaFrente'):
                raise ValueError('Las paredes ya existen. Deci cancelar casa.')
            self.mutate(doc, 'Paredes', lambda: self.walls(doc, floor, self.values['height'], value))
            self.pending = None
            return self.tell('Cuatro paredes listas. Deci poner puerta al frente.')

    @staticmethod
    def current():
        import FreeCAD as App
        doc = App.ActiveDocument
        floor = doc.getObject('CasaPiso') if doc else None
        if floor is None or not hasattr(floor, 'DemoVersion'):
            raise ValueError('Activa una casa de esta demo o deci crear piso de cuatro por cuatro.')
        return doc, floor

    @staticmethod
    def box(l, w, h, x=0, y=0, z=0):
        import Part
        from FreeCAD import Vector
        return Part.makeBox(l, w, h, Vector(x, y, z))

    @staticmethod
    def feature(doc, name, label, shape, color):
        if shape.isNull() or not shape.isValid() or shape.Volume <= 0:
            raise ValueError('No se pudo generar un solido valido: ' + label)
        obj = doc.addObject('Part::Feature', name)
        obj.Label = label
        obj.Shape = shape
        obj.ViewObject.ShapeColor = color
        obj.ViewObject.LineColor = (0.25, 0.25, 0.25)
        return obj

    def floor(self, length, width, thickness):
        import FreeCAD as App
        self.check_size(length, width)
        doc = App.newDocument('CasaDemo')
        floor = self.feature(doc, 'CasaPiso', 'Piso', self.box(length, width, thickness), (0.65, 0.65, 0.61))
        for name, value in [('Largo', length), ('Ancho', width), ('Espesor', thickness), ('AlturaPared', 0), ('EspesorPared', 0)]:
            floor.addProperty('App::PropertyLength', name, 'Demo casa')
            setattr(floor, name, value)
            floor.setEditorMode(name, 1)
        floor.addProperty('App::PropertyString', 'DemoVersion', 'Demo casa')
        floor.DemoVersion = '1'
        doc.recompute()
        self.view()

    @staticmethod
    def dimensions(floor):
        return [float(getattr(floor, name).Value) for name in ('Largo', 'Ancho', 'Espesor', 'AlturaPared', 'EspesorPared')]

    def walls(self, doc, floor, height, thickness):
        l, w, z, _, _ = self.dimensions(floor)
        color = (0.93, 0.86, 0.70)
        for name, label, shape in [
            ('CasaFrente', 'Pared del frente', self.box(l, thickness, height, z=z)),
            ('CasaFondo', 'Pared del fondo', self.box(l, thickness, height, y=w-thickness, z=z)),
            ('CasaLateralIzquierdo', 'Pared izquierda', self.box(thickness, w-2*thickness, height, y=thickness, z=z)),
            ('CasaLateralDerecho', 'Pared derecha', self.box(thickness, w-2*thickness, height, x=l-thickness, y=thickness, z=z))]:
            self.feature(doc, name, label, shape, color)
        floor.AlturaPared = height
        floor.EspesorPared = thickness

    def opening(self, doc, x, z, width, height, thickness):
        self.cut_opening(doc.getObject('CasaFrente'), self.box(width, thickness+20, height, x, -10, z))

    @staticmethod
    def cut_opening(wall, cutter):
        result = wall.Shape.cut(cutter).removeSplitter()
        if not result.isValid() or result.Volume >= wall.Shape.Volume:
            raise ValueError('No se pudo recortar la abertura.')
        wall.Shape = result

    def door(self, doc, floor):
        l, w, z, h, t = self.dimensions(floor)
        x = (l-900)/2
        self.opening(doc, x, z, 900, 2100, t)
        frame = self.box(900, 80, 2100, x, 25, z).cut(self.box(780, 100, 2040, x+60, 15, z))
        self.feature(doc, 'CasaMarcoPuerta', 'Marco de puerta', frame, (0.34, 0.20, 0.10))
        self.feature(doc, 'CasaPuerta', 'Puerta', self.box(780, 45, 2030, x+60, 70, z), (0.58, 0.32, 0.14))
        import Part
        from FreeCAD import Vector
        self.feature(doc, 'CasaPicaporte', 'Picaporte', Part.makeSphere(30, Vector(x+720, 60, z+1000)), (0.85, 0.68, 0.25))

    def windows(self, doc, floor, positions):
        l, w, z, h, t = self.dimensions(floor)
        locations = {
            'Izquierda': (l * 0.22, 'CasaFrente', 'izquierda del frente'),
            'Derecha': (l * 0.78, 'CasaFrente', 'derecha del frente'),
            'CostadoDerecho': (w / 2, 'CasaLateralDerecho', 'del costado derecho'),
            'CostadoIzquierdo': (w / 2, 'CasaLateralIzquierdo', 'del costado izquierdo'),
            'Fondo': (l / 2, 'CasaFondo', 'del fondo'),
        }
        for name in positions:
            center, wall_name, label = locations[name]
            x, bottom = center-350, z+1050
            def window_box(width, depth, height, along, inset, vertical):
                if wall_name == 'CasaLateralDerecho':
                    return self.box(depth, width, height, l - inset - depth, along, vertical)
                if wall_name == 'CasaLateralIzquierdo':
                    return self.box(depth, width, height, inset, along, vertical)
                if wall_name == 'CasaFondo':
                    return self.box(width, depth, height, along, w - inset - depth, vertical)
                return self.box(width, depth, height, along, inset, vertical)

            wall = doc.getObject(wall_name)
            self.cut_opening(wall, window_box(700, t+20, 950, x, -10, bottom))
            frame = window_box(700, 80, 950, x, 25, bottom).cut(window_box(600, 100, 850, x+50, 15, bottom+50))
            frame = frame.fuse(window_box(40, 80, 850, x+330, 25, bottom+50)).removeSplitter()
            self.feature(doc, 'CasaVentana'+name, 'Ventana '+label, frame, (0.95, 0.95, 0.92))
            glass = self.feature(doc, 'CasaVidrio'+name, 'Vidrio '+label, window_box(600, 12, 850, x+50, 70, bottom+50), (0.40, 0.74, 0.91))
            glass.ViewObject.Transparency = 65

    def roof(self, doc, floor):
        import Part
        from FreeCAD import Vector
        l, w, z, h, t = self.dimensions(floor)
        eave = z+h
        ridge = eave + l/2*math.tan(math.radians(30))
        def prism(points, y, depth):
            vertices = [Vector(x, y, zz) for x, zz in points]
            return Part.Face(Part.makePolygon(vertices+[vertices[0]])).extrude(Vector(0, depth, 0))
        triangle = [(0,eave), (l,eave), (l/2,ridge)]
        for name, y in [('Frente',0), ('Fondo',w-t)]:
            self.feature(doc, 'CasaTimpano'+name, 'Cierre triangular '+name.lower(), prism(triangle,y,t), (0.93,0.86,0.70))
        outer = eave-250*math.tan(math.radians(30))
        left = [(-250,outer), (l/2,ridge), (l/2,ridge+120), (-250,outer+120)]
        right = [(l/2,ridge), (l+250,outer), (l+250,outer+120), (l/2,ridge+120)]
        for name, points in [('Izquierdo',left), ('Derecho',right)]:
            self.feature(doc, 'CasaTecho'+name, 'Techo '+name.lower(), prism(points,-250,w+500), (0.65,0.17,0.10))

    def mutate(self, doc, name, action):
        doc.openTransaction('Demo casa: '+name)
        try:
            action()
            doc.recompute()
            doc.commitTransaction()
        except Exception:
            doc.abortTransaction()
            raise
        self.view()

    @staticmethod
    def view():
        import FreeCADGui as Gui
        Gui.activeDocument().activeView().viewAxonometric()
        Gui.activeDocument().activeView().fitAll()


def install(browser, refresh_grammar, *, enabled=False):
    """Add demo commands at every navigation level and expose them to Vosk."""
    if hasattr(browser, '_house_demo'):
        return browser._house_demo
    demo = HouseDemo(refresh_grammar=refresh_grammar)
    demo.enabled = enabled
    browser._house_demo = demo
    original_process = browser.ProcessPhrase
    original_grammar = browser.GetSpokenPhrases
    start = 'activar demo casa'
    stop = 'salir de la demo casa'

    def spoken_phrases():
        phrases = set(original_grammar()) | {start}
        if demo.enabled:
            phrases.update(demo.grammar())
            phrases.add(stop)
            phrases.update(demo.choice_words or ())
        return sorted(phrases)

    browser.GetSpokenPhrases = spoken_phrases

    def process(phrase):
        from navigation.browser import BrowserResult
        try:
            command = normalize(phrase)
            if command == start:
                demo.enabled = True
                refresh_grammar()
                return BrowserResult(True, 'house_demo', demo.tell('Demo activa. Decí «ayuda casa» o «ayuda habitaciones».'))
            if not demo.enabled:
                return original_process(phrase)
            if command == stop:
                demo.enabled = False
                demo.cancel_question()
                if demo.label is not None:
                    demo.label.parentWidget().hide()
                return BrowserResult(True, 'house_demo', 'Demo de casa desactivada.')
            message = None
            if (not demo.pending and browser.CurrentContextName == 'Modify'
                    and command in ('mover objeto', 'cambiar posicion')):
                message = demo.showcase.move_selection()
            if message is None:
                message = demo.handle(phrase)
            if message is None:
                return original_process(phrase)
            return BrowserResult(True, 'house_demo', message)
        except (ValueError, RuntimeError) as exc:
            message = str(exc)
            if demo.pending:
                message += '\n' + demo.question
            demo.tell(message)
            return BrowserResult(False, 'house_demo', message)
    browser.ProcessPhrase = process
    import demo_extension
    demo_extension.install_extra(demo)
    return demo
