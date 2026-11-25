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

"""Assembly example: an M30 threaded rod with two nuts that turn along its thread (screw joint)."""

try:
    import Part
except ImportError:
    Part = None
try:
    import Sketcher
except ImportError:
    Sketcher = None
try:
    from FreeCAD import Vector
except ImportError:
    Vector = None

from ._bulontuerca import _assemblyHelpers, _connectors, _pick, _pickBody
from ._common import activeDoc, attachAt, fitView, lastOfType, setView
from ._words import down, nextItem, no, numbers, send, yes

TITLE = {
    "es": "Varilla roscada M30 con tuercas",
    "en": "M30 threaded rod with nuts",
}

# Rosca métrica M30 de paso grueso (ISO 261): paso 3,5 mm y diámetro mayor 30 mm. El eje va por Z.
PITCH = 3.5
MAJOR_RADIUS = 15  # cresta de la rosca
CORE_RADIUS = 13  # núcleo del vástago, un poco menos que el diámetro menor (26,2 mm)
ROD_LENGTH = 100
THREAD_START = 2  # altura donde empieza la hélice
THREAD_HEIGHT = 96  # 27 vueltas, hasta z = 98

# Perfil de la rosca (triángulo de 60° incluidos) en el plano XZ: la base se hunde en el núcleo
# para que la hélice quede fundida con él y la cresta llega a 15.
PROFILE = ((12.5, 0.6), (12.5, 3.4), (15, 2))

# Tuerca hexagonal M30 (DIN 934): 46 mm entre caras (radio circunscrito 26,5) y 24 mm de alto.

NUT_RADIUS = 26.5
NUT_HEIGHT = 24
NUT_X = 50
NUT_CENTER_Z = NUT_HEIGHT // 2
HOLE_HEIGHT = 30


def _bodies() -> list:
    return [obj for obj in activeDoc().Objects if obj.TypeId == "PartDesign::Body"]


def _links() -> list:
    """The assembly links in the order they were inserted: the rod, the first nut and the second nut."""
    return [obj for obj in activeDoc().Objects if obj.TypeId == "App::Link"]


def _rod() -> None:
    doc = activeDoc()
    body = doc.addObject("PartDesign::Body", "Body")
    core = doc.addObject("PartDesign::AdditiveCylinder", "Core")
    core.Radius = CORE_RADIUS
    core.Height = ROD_LENGTH
    body.addObject(core)
    # el cilindro nace con su base en el origen: el centro dictado (0, 0, 50) queda a media altura
    attachAt(body, core, 0, 0, 0)
    doc.recompute()
    fitView()


def _threadSketch() -> None:
    doc = activeDoc()
    body = _bodies()[0]
    plane = next(item for item in body.Origin.OriginFeatures if item.Role == "XZ_Plane")
    sketch = body.newObject("Sketcher::SketchObject", "ThreadProfile")
    sketch.AttachmentSupport = [(plane, "")]
    sketch.MapMode = "FlatFace"
    doc.recompute()
    fitView()


def _threadProfile() -> None:
    doc = activeDoc()
    sketch = lastOfType(doc, "Sketcher::SketchObject")
    corners = [Vector(x, z, 0) for x, z in PROFILE]
    for index in range(3):
        sketch.addGeometry(Part.LineSegment(corners[index], corners[(index + 1) % 3]), False)
    for index in range(3):
        sketch.addConstraint(Sketcher.Constraint("Coincident", index, 2, (index + 1) % 3, 1))
    doc.recompute()
    fitView()


def _thread() -> None:
    doc = activeDoc()
    body = _bodies()[0]
    sketch = lastOfType(doc, "Sketcher::SketchObject")
    helix = body.newObject("PartDesign::AdditiveHelix", "Thread")
    helix.Profile = sketch
    helix.ReferenceAxis = (sketch, ["V_Axis"])
    helix.Mode = "pitch-height-angle"
    helix.Pitch = PITCH
    helix.Height = THREAD_HEIGHT
    sketch.Visibility = False
    doc.recompute()
    if not helix.isValid():
        raise RuntimeError("No se pudo hacer la rosca: seguí los cuadros en orden.")
    fitView()


def _dimension() -> None:
    # la misma función que ejecuta el comando «cota» del diccionario (3D: hay un sólido)
    from measure import _dimension3d

    _dimension3d(MAJOR_RADIUS, 0, THREAD_START, MAJOR_RADIUS, 0, THREAD_START + PITCH)
    activeDoc().recompute()
    fitView()


def _nut() -> None:
    doc = activeDoc()
    body = doc.addObject("PartDesign::Body", "Body")
    prism = doc.addObject("PartDesign::AdditivePrism", "Nut")
    prism.Polygon = 6
    prism.Circumradius = NUT_RADIUS
    prism.Height = NUT_HEIGHT
    body.addObject(prism)
    attachAt(body, prism, NUT_X, 0, NUT_CENTER_Z - NUT_HEIGHT / 2)
    doc.recompute()
    fitView()


def _nutHole() -> None:
    doc = activeDoc()
    body = _bodies()[1]
    hole = doc.addObject("PartDesign::SubtractiveCylinder", "NutHole")
    hole.Radius = MAJOR_RADIUS
    hole.Height = HOLE_HEIGHT
    body.addObject(hole)
    attachAt(body, hole, NUT_X, 0, NUT_CENTER_Z - HOLE_HEIGHT / 2)
    doc.recompute()
    fitView()


def _createAssembly() -> None:
    doc = activeDoc()
    assembly = doc.addObject("Assembly::AssemblyObject", "Assembly")
    assembly.Type = "Assembly"
    assembly.newObject("Assembly::JointGroup", "Joints")
    doc.recompute()
    fitView()


def _insertLink(position: int):
    def action() -> None:
        doc = activeDoc()
        assembly = lastOfType(doc, "Assembly::AssemblyObject")
        # _InsertLink oculta el cuerpo original: se ven solo los vínculos del ensamblaje
        _assemblyHelpers()._InsertLink(doc, assembly, _bodies()[position])
        fitView()

    return action


def _link(position: int):
    """Return the assembly link number ``position``: 0 is the rod, 1 and 2 are the nuts."""
    links = _links()
    if len(links) <= position:
        raise RuntimeError("Falta el vínculo de la pieza: seguí los cuadros en orden.")
    return links[position]


def _ground() -> None:
    parametric = _assemblyHelpers()
    import JointObject

    doc = activeDoc()
    assembly = parametric._ActiveAssembly(doc)
    # lo mismo que hace «anclar pieza»
    feature = parametric._JointGroup(assembly).newObject("App::FeaturePython", "GroundedJoint")
    JointObject.GroundedJoint(feature, _link(0))
    doc.recompute()
    parametric._RegisterObject(feature)


def _faceName(link, label: str) -> str:
    """Name of the face of ``link`` that the voice list shows as ``label``."""
    for name, shown in _connectors().listConnectors(link):
        if shown == label:
            return name
    raise RuntimeError(f"La pieza no tiene la cara «{label}».")


def _facePosition(link, label: str) -> int:
    names = [name for name, _label in _connectors().listConnectors(link)]
    return names.index(_faceName(link, label))


def _screw(nut: int, label: str):
    """Return the action that joins the nut number ``nut`` to the rod by their faces called ``label``."""

    def action() -> None:
        parametric = _assemblyHelpers()
        doc = activeDoc()
        links = [_link(0), _link(nut)]
        # lo mismo que hace «junta de tornillo»: cada pieza se une por la cara elegida
        joint = parametric._CreateJoint("Screw", doc, links, [_faceName(link, label) for link in links])
        if joint is None:
            raise RuntimeError("No se pudo crear la junta: seguí los cuadros en orden.")
        joint.Distance = PITCH
        parametric._AlignForScrew(doc, parametric._ActiveAssembly(doc), joint, links)
        doc.recompute()
        parametric._RegisterObject(joint)

    return action


def _screwWords(language: str, nut: int, label: str) -> tuple:
    """Words of a screw joint: the pitch, the two parts from the list and the face of each one."""
    rod, nutLink = _link(0), _link(nut)
    return (
        numbers(language, PITCH)
        + _pick(language, rod, nutLink)
        + down(language, _facePosition(rod, label))
        + send(language)
        + down(language, _facePosition(nutLink, label))
        + send(language)
    )


def _solve() -> None:
    doc = activeDoc()
    assembly = lastOfType(doc, "Assembly::AssemblyObject")
    if assembly.solve() != 0:
        raise RuntimeError("El ensamblaje no se pudo resolver.")
    doc.recompute()
    # las dos tuercas tienen que estar sobre el eje de la varilla
    for position in (1, 2):
        center = _link(position).Shape.BoundBox.Center
        if abs(center.x) > 0.01 or abs(center.y) > 0.01:
            raise RuntimeError("El ensamblaje no encastró las tuercas en la varilla.")
    fitView()


def _isometric() -> None:
    setView("isometric")


def steps() -> list:
    """Return the frames of the threaded rod example."""
    from InputPrompts.ExampleStep import ExampleStep

    def say(es, en):
        return {"es": es, "en": en}

    return [
        ExampleStep(
            Text=say(
                "La varilla roscada M30: primero el núcleo, un cilindro de radio 13 y 100 de alto, con el centro en (0, 0, 50).",
                "The M30 threaded rod: first the core, a cylinder with radius 13 and height 100, centred at (0, 0, 50).",
            ),
            Path=say(
                ("banco", "diseño", "sumar", "cilindro"),
                ("workbench", "design", "add", "cylinder"),
            ),
            Values=lambda language: numbers(language, CORE_RADIUS, ROD_LENGTH, 0, 0, ROD_LENGTH // 2),
            Action=_rod,
        ),
        ExampleStep(
            Text=say(
                "Para la rosca hace falta el dibujo de un filete. Boceto nuevo sobre el plano XZ (es el segundo de la lista: «abajo» una vez y «enviar»).",
                "The thread needs a drawing of one thread ridge. New sketch on the XZ plane (second in the list: “down” once and “send”).",
            ),
            Path=say(("base", "nuevo boceto"), ("base", "new sketch")),
            Values=lambda language: down(language, 1) + send(language),
            Action=_threadSketch,
        ),
        ExampleStep(
            Text=say(
                "Dibujá el filete: un triángulo por vértices, (12,5; 0,6), (12,5; 3,4) y (15; 2). Es el perfil de 60° de la rosca métrica: la base se hunde en el núcleo y la cresta llega a 15, o sea, 30 de diámetro.",
                "Draw the thread ridge: a triangle by vertices, (12.5, 0.6), (12.5, 3.4) and (15, 2). It is the 60° profile of the metric thread: the base sinks into the core and the crest reaches 15, that is, 30 in diameter.",
            ),
            Path=say(
                ("geometría", "triángulo", "triángulo por vértices"),
                ("geometry", "triangle", "triangle by vertices"),
            ),
            Values=lambda language: numbers(language, *(value for corner in PROFILE for value in corner)),
            Action=_threadProfile,
        ),
        ExampleStep(
            Text=say(
                "Cerrá el croquis y enrollá el filete en una hélice: paso 3,5 (el paso grueso de la M30) y altura 96, o sea, 27 vueltas. Después elegís el dibujo de la lista (es el único: «enviar»).",
                "Close the sketch and wind the ridge into a helix: pitch 3.5 (the coarse pitch of the M30) and height 96, that is, 27 turns. Then pick the drawing from the list (it is the only one: “send”).",
            ),
            Path=say(
                ("cerrar croquis", "banco", "diseño", "sumar", "hélice"),
                ("close sketch", "workbench", "design", "add", "additive helix"),
            ),
            Values=lambda language: numbers(language, PITCH, THREAD_HEIGHT) + send(language),
            Action=_thread,
        ),
        ExampleStep(
            Text=say(
                "Medí el paso: de una cresta a la siguiente, de (15, 0, 2) a (15, 0, 5,5). La cota marca 3,5 mm, lo que avanza la rosca en cada vuelta.",
                "Measure the pitch: from one crest to the next, from (15, 0, 2) to (15, 0, 5.5). The dimension reads 3.5 mm, what the thread advances in every turn.",
            ),
            Path=say(("cota",), ("measure",)),
            Values=lambda language: numbers(language, MAJOR_RADIUS, 0, THREAD_START, MAJOR_RADIUS, 0, THREAD_START + PITCH),
            Action=_dimension,
        ),
        ExampleStep(
            Text=say(
                "La tuerca es otra pieza: un prisma de 6 lados, radio 26,5 (46 entre caras, como la DIN 934) y 24 de alto, centro en (50, 0, 12), aparte de la varilla. Decí «sí» a «¿cuerpo nuevo?».",
                "The nut is another part: a 6-sided prism, radius 26.5 (46 across flats, as in DIN 934) and 24 high, centred at (50, 0, 12), away from the rod. Say “yes” to “new body?”.",
            ),
            Path=say(
                ("banco", "diseño", "sumar", "prisma"),
                ("workbench", "design", "add", "prism"),
            ),
            Values=lambda language: numbers(language, 6, NUT_RADIUS, NUT_HEIGHT, NUT_X, 0, NUT_CENTER_Z) + yes(language),
            Action=_nut,
        ),
        ExampleStep(
            Text=say(
                "Agujereá la tuerca: un cilindro sustractivo de radio 15 (el diámetro mayor de la rosca) y 30 de alto, centro en (50, 0, 12). Primero «subir» un nivel, porque estás en Sumar. En la lista de cuerpos, «avanzar» una vez para elegir la tuerca.",
                "Drill the nut: a subtractive cylinder with radius 15 (the major diameter of the thread) and height 30, centred at (50, 0, 12). First go “up” one level, since you are in Add. In the list of bodies, say “next” once to pick the nut.",
            ),
            Path=say(
                ("subir", "cortar", "cilindro"),
                ("up", "cut", "cylinder"),
            ),
            Values=lambda language: numbers(language, MAJOR_RADIUS, HOLE_HEIGHT, NUT_X, 0, NUT_CENTER_Z)
            + nextItem(language, 1)
            + send(language),
            Action=_nutHole,
        ),
        ExampleStep(
            Text=say(
                "Ahora el ensamblaje: creá uno nuevo.",
                "Now the assembly: create a new one.",
            ),
            Path=say(
                ("banco", "ensamblaje", "crear ensamblaje"),
                ("workbench", "assembly", "create assembly"),
            ),
            Action=_createAssembly,
        ),
        ExampleStep(
            Text=say(
                "Insertá la varilla en el ensamblaje: en la lista de piezas elegí el primer cuerpo con «enviar».",
                "Insert the rod into the assembly: in the list of parts pick the first body with “send”.",
            ),
            Path=say(("insertar vínculo",), ("insert link",)),
            Values=lambda language: _pickBody(language, 0),
            Action=_insertLink(0),
        ),
        ExampleStep(
            Text=say(
                "Insertá la tuerca: «avanzar» una vez para elegir el segundo cuerpo. Se pone a la derecha de la varilla, sin pisarla.",
                "Insert the nut: say “next” once to pick the second body. It is placed to the right of the rod, without overlapping it.",
            ),
            Path=say(("insertar vínculo",), ("insert link",)),
            Values=lambda language: _pickBody(language, 1),
            Action=_insertLink(1),
        ),
        ExampleStep(
            Text=say(
                "Insertá la misma tuerca otra vez: es la segunda tuerca de la varilla. Elegí de nuevo el segundo cuerpo.",
                "Insert the same nut again: it is the rod's second nut. Pick the second body once more.",
            ),
            Path=say(("insertar vínculo",), ("insert link",)),
            Values=lambda language: _pickBody(language, 1),
            Action=_insertLink(1),
        ),
        ExampleStep(
            Text=say(
                "Anclá la varilla: el solver la deja quieta y mueve las tuercas. La lista muestra primero los cuerpos y después los vínculos: «avanzar» hasta el vínculo de la varilla y «enviar».",
                "Ground the rod: the solver keeps it still and moves the nuts. The list shows the bodies first and then the links: say “next” up to the rod's link and “send”.",
            ),
            Path=say(("anclar pieza",), ("ground part",)),
            Values=lambda language: _pick(language, _link(0)),
            Action=_ground,
        ),
        ExampleStep(
            Text=say(
                "Unila con la primera tuerca con una junta de tornillo de paso 3,5: la tuerca gira y avanza por la rosca. Elegí el vínculo de la varilla y el de la tuerca; después, por dónde se une cada uno: la cara inferior de la varilla y la de la tuerca (se baja en la lista de caras hasta ella y «enviar»). La tuerca salta al extremo de abajo.",
                "Join it to the first nut with a screw joint with pitch 3.5: the nut turns and advances along the thread. Pick the rod's link and the nut's; then where each one joins: the bottom face of the rod and that of the nut (go down the list of faces to it and “send”). The nut jumps to the lower end.",
            ),
            Path=say(("junta de tornillo",), ("screw joint",)),
            Values=lambda language: _screwWords(language, 1, "Cara inferior"),
            Action=_screw(1, "Cara inferior"),
        ),
        ExampleStep(
            Text=say(
                "Lo mismo con la segunda tuerca, pero por la cara superior de la varilla y la de la tuerca: va al extremo de arriba.",
                "The same with the second nut, but through the top face of the rod and that of the nut: it goes to the upper end.",
            ),
            Path=say(("junta de tornillo",), ("screw joint",)),
            Values=lambda language: _screwWords(language, 2, "Cara superior"),
            Action=_screw(2, "Cara superior"),
        ),
        ExampleStep(
            Text=say(
                "Resolvé el ensamblaje para comprobar que todo encaja: las dos tuercas quedan sobre la rosca, una en cada punta.",
                "Solve the assembly to check that everything fits: both nuts stay on the thread, one at each end.",
            ),
            Path=say(("resolver",), ("solve",)),
            Action=_solve,
        ),
        ExampleStep(
            Text=say(
                "Mirá el conjunto terminado: decí «tres de» (vista isométrica). Para moverlo, arrastrá una tuerca con el mouse: gira y avanza 3,5 mm por vuelta, y la cota del paso sigue a la vista. Después decí «enviar» para cerrar el ejemplo.",
                "See the finished set: say “isometric”. To move it, drag a nut with the mouse: it turns and advances 3.5 mm per turn, and the pitch dimension stays in view. Then say “send” to close the example.",
            ),
            Path=say(("tres de",), ("isometric",)),
            Action=_isometric,
        ),
    ]