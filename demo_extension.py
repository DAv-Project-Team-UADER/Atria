"""Ampliacion de DEMOATRIA: plantas repetibles, techo superior y seleccion por nombre.

Solo se activa dentro de la demo de casa; no modifica las herramientas BIM externas.
"""
from __future__ import annotations

import re
import unicodedata
import demo_house

CMDS = {
    'crear entrepiso': 'slab', 'poner entrepiso': 'slab', 'crear losa de entrepiso': 'slab',
    'crear siguiente entrepiso': 'slab', 'agregar piso': 'slab',
    'levantar segundo piso': 'walls', 'crear segundo piso': 'walls',
    'levantar siguiente piso': 'walls', 'levantar otro piso': 'walls',
    'poner cuatro paredes arriba': 'walls', 'levantar cuatro paredes arriba': 'walls',
    'poner techo plano': 'flat', 'crear techo plano': 'flat', 'poner techo recto': 'flat',
    'poner techo a dos aguas': 'pitched', 'crear techo a dos aguas': 'pitched',
    'construir techo': 'pitched',
    'ocultar techo': 'hide', 'mostrar techo': 'show', 'quitar techo': 'remove_roof',
    'poner ventana': 'window', 'colocar ventana': 'window',
    'insertar ventana': 'window', 'agregar ventana': 'window',
    'seleccionar por nombre': 'select_ask', 'elegir por nombre': 'select_ask',
    'ayuda ampliacion': 'help', 'ayuda ampliación': 'help',
}
WALLS = {
    'frontal': 'Frente', 'frente': 'Frente', 'pared frontal': 'Frente',
    'derecha': 'LateralDerecho', 'pared derecha': 'LateralDerecho', 'costado derecho': 'LateralDerecho',
    'trasera': 'Fondo', 'fondo': 'Fondo', 'pared trasera': 'Fondo',
    'izquierda': 'LateralIzquierdo', 'pared izquierda': 'LateralIzquierdo', 'costado izquierdo': 'LateralIzquierdo',
}
WALL_NICK = {'Frente': 'frontal', 'Fondo': 'trasera', 'LateralDerecho': 'derecha', 'LateralIzquierdo': 'izquierda'}
ORDINALS = {1:'planta baja', 2:'segundo piso', 3:'tercer piso', 4:'cuarto piso',
            5:'quinto piso', 6:'sexto piso', 7:'septimo piso', 8:'octavo piso',
            9:'noveno piso', 10:'decimo piso'}
LEVEL_PHRASES = {'planta baja':1, 'baja':1, 'primer piso':1, 'planta alta':2,
                 'alta':2, 'segundo piso':2, 'tercer piso':3, 'cuarto piso':4,
                 'quinto piso':5, 'sexto piso':6, 'septimo piso':7,
                 'octavo piso':8, 'noveno piso':9, 'decimo piso':10,
                 'ultimo piso':-1, 'ultima planta':-1, 'arriba':-1}


def norm(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', str(text).lower()) if not unicodedata.combining(c)).strip()


def ask_level(demo, maximum, on_accept):
    aliases = {f'nivel {level}': level for level in range(1, maximum + 1)}
    aliases.update({word: maximum if level == -1 else level
                    for word, level in LEVEL_PHRASES.items() if level <= maximum})
    labels = {level: ORDINALS.get(level, f'nivel {level}').capitalize()
              for level in range(1, maximum + 1)}
    return demo.ask_options('window_level', '¿En qué piso va la ventana?', aliases, on_accept, labels)


def _wall_name(n, key):
    return 'Casa'+key if n == 1 else 'CasaAlta'+key if n == 2 else 'CasaNivel'+str(n)+key


def _slab_name(n):
    return 'CasaPiso' if n == 1 else 'CasaPisoSuperior' if n == 2 else 'CasaNivel'+str(n)+'Piso'


def levels(doc):
    # Ultimo nivel de paredes totalmente construido, sin inferir por cantidad de objetos.
    n = 1
    while doc.getObject(_wall_name(n+1,'Frente')) is not None:
        n += 1
    return n


def _dims(demo, floor):
    return demo.dimensions(floor)  # largo, fondo, espesor losa inicial, alto, espesor paredes


def _wall_z(floor, n, demo):
    _l,_w, slab,h,_t = _dims(demo, floor)
    return slab + (n-1)*(h+200.0)


def _top_z(floor, n, demo):
    _l,_w,slab,h,_t = _dims(demo,floor)
    return slab + n*h + (n-1)*200.0


def _roof_objects(doc):
    return [obj for obj in doc.Objects if obj.Name.startswith('CasaTecho')]


def _make_slab(demo, doc, floor, n):
    l,w,*_ = _dims(demo,floor)
    z = _top_z(floor,n-1,demo)
    return demo.feature(doc,_slab_name(n),f'Entrepiso nivel {n}',demo.box(l,w,200.0,0,0,z),(.67,.68,.69))


def _make_walls(demo,doc,floor,n):
    l,w,_,h,t = _dims(demo,floor)
    z = _wall_z(floor,n,demo)
    color=(.91,.84,.70)
    for key, label, shape in (
        ('Frente','frontal',demo.box(l,t,h,0,0,z)),
        ('Fondo','trasera',demo.box(l,t,h,0,w-t,z)),
        ('LateralIzquierdo','izquierda',demo.box(t,w-2*t,h,0,t,z)),
        ('LateralDerecho','derecha',demo.box(t,w-2*t,h,l-t,t,z)),
    ):
        demo.feature(doc,_wall_name(n,key),f'Pared {label} - nivel {n}',shape,color)


def _make_flat(demo,doc,floor):
    n=levels(doc)
    l,w,*_ = _dims(demo,floor)
    z=_top_z(floor,n,demo)
    return demo.feature(doc,'CasaTechoPlano',f'Techo plano nivel {n}',demo.box(l,w,200.0,0,0,z),(.67,.68,.69))


def _make_pitch(demo,doc,floor):
    import math
    import Part
    from FreeCAD import Vector
    n=levels(doc)
    l,w,_,_,t=_dims(demo,floor)
    # Usar la altura REAL de las cuatro paredes del ultimo nivel.
    # No confiar en la altura de la planta baja ni en un calculo teorico.
    keys=('Frente','Fondo','LateralIzquierdo','LateralDerecho')
    walls=[doc.getObject(_wall_name(n,key)) for key in keys]
    if any(obj is None for obj in walls):
        raise ValueError('Faltan paredes en el ultimo piso; termina ese nivel antes del techo.')
    eave=max(float(obj.Shape.BoundBox.ZMax) for obj in walls)
    ridge=eave+l/2*math.tan(math.radians(30))
    def prism(points,y,depth):
        vertices=[Vector(x,y,zz) for x,zz in points]
        return Part.Face(Part.makePolygon(vertices+[vertices[0]])).extrude(Vector(0,depth,0))
    triangle=[(0,eave),(l,eave),(l/2,ridge)]
    for name,y in (('Frente',0),('Fondo',w-t)):
        demo.feature(doc,'CasaTimpano'+name,f'Cierre triangular nivel {n} {name}',prism(triangle,y,t),(.93,.86,.70))
    outer=eave-250*math.tan(math.radians(30))
    sides=(('Izquierdo',[(-250,outer),(l/2,ridge),(l/2,ridge+120),(-250,outer+120)]),
           ('Derecho',[(l/2,ridge),(l+250,outer),(l+250,outer+120),(l/2,ridge+120)]))
    for key,points in sides:
        demo.feature(doc,'CasaTecho'+key,f'Techo a dos aguas nivel {n} {key}',prism(points,-250,w+500),(.65,.17,.10))


def _window(demo, doc, floor, wall_key, n):
    l,w,slab,h,t=_dims(demo,floor)
    wall=doc.getObject(_wall_name(n,wall_key))
    if wall is None:
        raise ValueError('No existen las cuatro paredes de esa planta.')
    unique=f'CasaVentanaNivel{n}{wall_key}'
    if doc.getObject(unique):
        raise ValueError('Ya hay una ventana nueva en esa pared y planta.')
    # Evita ventanas originales y puerta en zona coincidente de planta baja.
    if n==1:
        existing={ 'Frente': ('CasaVentanaIzquierda','CasaVentanaDerecha'),
                   'LateralDerecho': ('CasaVentanaCostadoDerecho',)}.get(wall_key,())
        if any(doc.getObject(x) for x in existing):
            raise ValueError('Esa pared ya tiene una ventana del modelo original. Elegi otra.')
    span = l if wall_key in ('Frente','Fondo') else w
    ww,wh=700.,950.
    center=span*(.25 if wall_key=='Frente' else .5)
    begin=center-ww/2
    bottom=_wall_z(floor,n,demo)+1050
    if wh+1050 >= h:
        raise ValueError('La pared es demasiado baja para esta ventana.')
    if wall_key=='Frente' and n==1 and doc.getObject('CasaPuerta') and center+ww/2 >= (l-900)/2:
        raise ValueError('No entra junto a la puerta frontal. Elegi otra pared.')
    if wall_key=='Frente':
        opening=demo.box(ww,t+20,wh,begin,-10,bottom)
        box=lambda along,depth,z,width,dep,height:demo.box(width,dep,height,along,depth,z)
        inset=25
    elif wall_key=='Fondo':
        opening=demo.box(ww,t+20,wh,begin,w-t-10,bottom)
        box=lambda along,depth,z,width,dep,height:demo.box(width,dep,height,along,depth,z)
        inset=w-t+25
    elif wall_key=='LateralIzquierdo':
        opening=demo.box(t+20,ww,wh,-10,begin,bottom)
        box=lambda along,depth,z,width,dep,height:demo.box(dep,width,height,depth,along,z)
        inset=25
    else:
        opening=demo.box(t+20,ww,wh,l-t-10,begin,bottom)
        box=lambda along,depth,z,width,dep,height:demo.box(dep,width,height,depth,along,z)
        inset=l-t+25
    demo.cut_opening(wall, opening)
    b,depth=55.,55.
    frame=box(begin,inset,bottom,ww,depth,b)
    frame=frame.fuse(box(begin,inset,bottom+wh-b,ww,depth,b))
    frame=frame.fuse(box(begin,inset,bottom+b,b,depth,wh-2*b))
    frame=frame.fuse(box(begin+ww-b,inset,bottom+b,b,depth,wh-2*b))
    demo.feature(doc,unique,f'Ventana {WALL_NICK[wall_key]} nivel {n}',frame.removeSplitter(),(.96,.96,.93))
    glass=demo.feature(doc,unique+'Vidrio',f'Vidrio {WALL_NICK[wall_key]} nivel {n}',box(begin+b,inset+21,bottom+b,ww-2*b,12,wh-2*b),(.38,.72,.93))
    glass.ViewObject.Transparency=60


def _selection_options(doc):
    """Alias de voz para objetos del modelo: solo se elige si el nombre es unico."""
    options={}
    for obj in doc.Objects:
        k=obj.Name
        if k.startswith('Casa'):
            for name in (getattr(obj,'Label',''),k):
                alias=norm(name)
                if alias:
                    options.setdefault(alias,[]).append(obj)
    max_level=levels(doc)
    for n in range(1,max_level+1):
        for wall,key in WALLS.items():
            obj=doc.getObject(_wall_name(n,key))
            if obj:
                for phrase in (f'pared {wall} {ORDINALS.get(n,"nivel "+str(n))}',
                               f'{wall} {ORDINALS.get(n,"nivel "+str(n))}',
                               f'pared {wall} nivel {n}',f'{wall} nivel {n}'):
                    options.setdefault(norm(phrase),[]).append(obj)
                if n==max_level:
                    options.setdefault(norm('pared '+wall+' ultimo piso'),[]).append(obj)
                if n==1:
                    options.setdefault(norm('pared '+wall),[]).append(obj)
        slab=doc.getObject(_slab_name(n))
        if slab: options.setdefault(norm('piso '+str(n)),[]).append(slab)
    for name in ('CasaTechoPlano','CasaTechoIzquierdo','CasaTechoDerecho'):
        obj=doc.getObject(name)
        if obj:
            alias={'CasaTechoPlano':'techo plano','CasaTechoIzquierdo':'techo izquierdo',
                   'CasaTechoDerecho':'techo derecho'}[name]
            options.setdefault(alias,[]).append(obj)
    # Dedup aliases (same wall may be expressed in multiple terms).
    return {k:list({obj.Name:obj for obj in values}.values()) for k,values in options.items()}


def _select(doc, phrase):
    import FreeCADGui as Gui
    key=norm(phrase)
    options=_selection_options(doc)
    matches=options.get(key,[])
    if not matches:
        raise ValueError('No encontre ese nombre. Deci seleccionar por nombre para ver ejemplos.')
    if len(matches)>1:
        raise ValueError('Nombre ambiguo. Agrega la planta o el numero de nivel.')
    obj=matches[0]
    Gui.Selection.clearSelection()
    Gui.Selection.addSelection(obj)
    return obj


def install_extra(demo):
    if getattr(demo,'_extra_instalada',False):
        return demo
    demo._extra_instalada=True
    original_grammar=demo.grammar
    original_handle=demo.handle

    def grammar():
        phrases=set(original_grammar())|set(CMDS)|set(WALLS)|set(LEVEL_PHRASES)
        phrases.update({'frontal', 'derecha', 'trasera', 'izquierda', 'planta baja', 'ultimo piso', 'ultimo nivel'})
        # Alias estables: estos pueden pronunciarse sin recorrer los elementos.
        for n in range(1,11):
            for w in ('frontal','derecha','trasera','izquierda'):
                phrases.add(f'seleccionar pared {w} nivel {n}')
                phrases.add(f'pared {w} nivel {n}')
                if n in ORDINALS:
                    phrases.add('seleccionar pared '+w+' '+ORDINALS[n])
                    phrases.add('pared '+w+' '+ORDINALS[n])
        for wall in ('frontal','derecha','trasera','izquierda'):
            phrases.add('seleccionar pared '+wall)
            phrases.add('pared '+wall)
            phrases.add('seleccionar pared '+wall+' ultimo piso')
            phrases.add('pared '+wall+' ultimo piso')
        phrases.update(('seleccionar techo plano','seleccionar techo izquierdo',
                        'seleccionar techo derecho','seleccionar piso 1','seleccionar piso 2'))
        return sorted(phrases)

    def handle(phrase):
        p=norm(phrase)
        if demo.pending or demo.prompt:
            return original_handle(phrase)

        if p.startswith('seleccionar ') and p not in ('seleccionar','seleccionar por nombre'):
            # Solo capturar expresiones de objetos conocidas; el resto sigue en ATRIA.
            key=p[len('seleccionar '):]
            if key.startswith(('pared ','techo ','piso ')):
                doc,_=demo.current()
                obj=_select(doc,key)
                return demo.tell('Seleccionado: '+obj.Label+'.')

        action=CMDS.get(p)
        if action is None: return original_handle(phrase)
        if action=='help':
            return demo.tell('Crear entrepiso, levantar siguiente piso (repetible), poner techo plano, poner techo a dos aguas en ultimo piso, quitar techo, poner ventana, seleccionar por nombre.')
        doc,floor=demo.current()
        if action == 'select_ask':
            aliases = {word: matches[0].Name for word, matches in _selection_options(doc).items()
                       if len(matches) == 1}
            labels = {name: doc.getObject(name).Label for name in aliases.values()}

            def select(name):
                demo.showcase.require_active(doc)
                obj = _select(doc, name)
                demo.tell('Seleccionado: ' + obj.Label + '. Ya podés decir modificar y mover objeto.')

            return demo.ask_options('select_object', '¿Qué pieza querés seleccionar?', aliases, select, labels)
        if action == 'window':
            if not doc.getObject('CasaFrente'):
                raise ValueError('Primero crea las paredes.')

            def choose_wall(wall):
                demo.showcase.require_active(doc)

                def place(level):
                    demo.showcase.require_active(doc)
                    demo.mutate(doc, 'Ventana', lambda: _window(demo, doc, floor, wall, level))
                    demo.tell(f'Ventana en pared {WALL_NICK[wall]} nivel {level}.')

                maximum = levels(doc)
                if maximum == 1:
                    return place(1)
                return ask_level(demo, maximum, place)

            return demo.ask_options('window_wall', '¿En qué pared va la ventana?', WALLS, choose_wall)
        if action in ('hide','show'):
            roofs=_roof_objects(doc)
            if not roofs: return demo.tell('No hay techo colocado.')
            for obj in roofs: obj.ViewObject.Visibility=(action=='show')
            return demo.tell('Techo visible.' if action=='show' else 'Techo oculto.')
        if action=='remove_roof':
            roofs=_roof_objects(doc)
            if not roofs:return demo.tell('No hay techo que quitar.')
            def remove():
                for obj in roofs:doc.removeObject(obj.Name)
                for name in ('CasaTimpanoFrente','CasaTimpanoFondo'):
                    if doc.getObject(name):doc.removeObject(name)
            demo.mutate(doc,'Quitar techo',remove)
            return demo.tell('Techo quitado. Ya podes crear entrepiso para seguir subiendo.')
        if not doc.getObject('CasaFrente'):
            raise ValueError('Primero deci rodear piso de paredes.')
        n=levels(doc)
        if action=='slab':
            if _roof_objects(doc):
                raise ValueError('Primero deci quitar techo para continuar hacia arriba.')
            next_n=n+1
            if doc.getObject(_slab_name(next_n)):
                return demo.tell('Ya existe el entrepiso. Deci levantar siguiente piso.')
            demo.mutate(doc,'Entrepiso',lambda:_make_slab(demo,doc,floor,next_n))
            return demo.tell(f'Entrepiso para el nivel {next_n} listo. Deci levantar siguiente piso.')
        if action=='walls':
            if _roof_objects(doc):raise ValueError('Primero quita el techo.')
            next_n=n+1
            if not doc.getObject(_slab_name(next_n)):
                raise ValueError('Primero deci crear entrepiso.')
            demo.mutate(doc,'Paredes nivel '+str(next_n),lambda:_make_walls(demo,doc,floor,next_n))
            return demo.tell(f'Cuatro paredes del nivel {next_n} listas. Podes repetir crear entrepiso y levantar siguiente piso.')
        if action in ('flat','pitched'):
            name='Techo plano' if action=='flat' else 'Techo a dos aguas'
            fn=_make_flat if action=='flat' else _make_pitch
            # El comando actualiza el techo, incluso si uno anterior quedo
            # en planta baja: remueve piezas viejas y construye arriba.
            def replace_roof():
                for obj in list(_roof_objects(doc)):
                    doc.removeObject(obj.Name)
                for part_name in ('CasaTimpanoFrente','CasaTimpanoFondo'):
                    if doc.getObject(part_name):
                        doc.removeObject(part_name)
                fn(demo,doc,floor)
            demo.mutate(doc,name,replace_roof)
            return demo.tell(f'{name} actualizado sobre el nivel {n}, el ultimo con paredes. Para continuar, deci quitar techo.')
        return original_handle(phrase)

    # La ruta original de HouseDemo.roof tambien usa el ultimo piso.
    # Evita que otra frase antigua vuelva a crear el techo en planta baja.
    demo.roof=lambda doc,floor: _make_pitch(demo,doc,floor)
    demo.grammar=grammar
    demo.handle=handle
    import demo_rooms
    demo_rooms.install_room_functions(demo)
    return demo
