"""Habitaciones modulares para DEMOATRIA. Ejecutar solamente desde HouseDemo en GUI FreeCAD.

Cada nueva habitacion tiene losa y tres muros exteriores; el muro compartido
pertenece a la habitacion origen. La puerta comunicante se abre en ese muro.
No modifica ni reemplaza el algoritmo original de la casa central.
"""
from __future__ import annotations

import math
import re
import unicodedata

from demo_showcase import ROOF_SHORT, WINDOW_3D

DIRECTIONS = {
    'derecha': 'derecha', 'a la derecha':'derecha',
    'izquierda': 'izquierda', 'a la izquierda':'izquierda',
    'atras':'trasera', 'atrás':'trasera', 'trasera':'trasera',
    'hacia atras':'trasera', 'hacia atrás':'trasera',
}
SIDES = {'frontal':'Frente','frente':'Frente','derecha':'LateralDerecho',
         'trasera':'Fondo','fondo':'Fondo','izquierda':'LateralIzquierdo'}
REV = {'Frente':'frontal','LateralDerecho':'derecha','Fondo':'trasera','LateralIzquierdo':'izquierda'}
ROOM_CMDS = {
    'agregar habitacion': 'add_prompt',
    'agregar habitacion a la derecha': 'add_right',
    'agregar habitacion derecha': 'add_right',
    'ampliar a la derecha': 'add_right',
    'agregar habitacion a la izquierda': 'add_left',
    'agregar habitacion izquierda': 'add_left',
    'ampliar a la izquierda': 'add_left',
    'agregar habitacion atras': 'add_back',
    'agregar habitacion hacia atras': 'add_back',
    'agregar habitacion trasera': 'add_back',
    'ampliar hacia atras': 'add_back',
    'seleccionar habitacion': 'choose',
    'seleccionar habitacion principal': 'main',
    'seleccionar casa principal': 'main',
    'ver habitaciones': 'list',
    'listar habitaciones': 'list',
    'ayuda habitaciones': 'help',
}
ROOF_ACTIONS = {'poner techo plano':'flat','crear techo plano':'flat','poner techo recto':'flat',
                'poner techo a dos aguas':'pitch','crear techo a dos aguas':'pitch',
                'construir techo':'pitch'}
ROOF_ACTIONS.update(dict.fromkeys(ROOF_SHORT, 'pitch'))
OTHER = {'crear entrepiso':'slab','poner entrepiso':'slab','crear losa de entrepiso':'slab',
         'crear siguiente entrepiso':'slab','agregar piso':'slab',
         'levantar siguiente piso':'walls', 'levantar segundo piso':'walls',
         'crear segundo piso':'walls', 'levantar otro piso':'walls',
         'poner cuatro paredes arriba':'walls','levantar cuatro paredes arriba':'walls',
         'quitar techo':'remove','ocultar techo':'hide','mostrar techo':'show'}
OTHER.update(dict.fromkeys(WINDOW_3D, 'window'))


def norm(s):
    return ' '.join(''.join(c for c in unicodedata.normalize('NFKD',str(s).lower()) if not unicodedata.combining(c)).split())


def prefix(n): return 'CasaModulo'+str(n)
def floor_name(n): return prefix(n)+'Piso'
def wall_name(n, level, side): return prefix(n)+'Nivel'+str(level)+side
def slab_name(n, level): return prefix(n)+'Entrepiso'+str(level)
def roof_prefix(n): return prefix(n)+'Techo'


def props(obj):
    return (float(obj.ModuloX.Value),float(obj.ModuloY.Value),
            float(obj.ModuloLargo.Value),float(obj.ModuloFondo.Value),
            float(obj.ModuloEspesor.Value),float(obj.ModuloAltura.Value),
            float(obj.ModuloLosa.Value),obj.ModuloOrigen, str(obj.ModuloTipo))


def module_catalog(doc, demo):
    result={}
    central=doc.getObject('CasaPiso')
    if central:
        L,W,slab,H,t=demo.dimensions(central)
        result[0]={'idx':0,'x':0.,'y':0.,'l':L,'w':W,'slab':slab,'h':H,'t':t,
                   'parent':None,'side':None,'label':'habitacion principal'}
    for ob in doc.Objects:
        mat=re.fullmatch(r'CasaModulo(\d+)Piso',ob.Name)
        if not mat: continue
        n=int(mat.group(1))
        try:
            x,y,l,w,t,h,slab,parent,side=props(ob)
        except (AttributeError,ValueError):continue
        result[n]={'idx':n,'x':x,'y':y,'l':l,'w':w,'t':t,'h':h,'slab':slab,
                   'parent':int(parent),'side':side,'label':ob.Label.lower()}
    return result


def walls_level(doc, room):
    if room['idx']==0:
        from demo_extension import levels
        return levels(doc)
    n=1
    while doc.getObject(wall_name(room['idx'],n+1,'Frente')) is not None or doc.getObject(wall_name(room['idx'],n+1,'Fondo')) is not None:
        n+=1
    return n


def wall_z(room,n): return room['slab']+(n-1)*(room['h']+200.)
def top_z(room,n): return wall_z(room,n)+room['h']


def room_wall(doc,room,level,side):
    if room['idx']==0:
        from demo_extension import _wall_name
        return doc.getObject(_wall_name(level,side))
    return doc.getObject(wall_name(room['idx'],level,side))


def _module_position(parent, direction, l, w):
    x,y=parent['x'],parent['y']
    if direction=='derecha': return x+parent['l'],y
    if direction=='izquierda': return x-l,y
    return x,y+parent['w']


def _overlap(a,b,eps=0.01):
    return min(a['x']+a['l'],b['x']+b['l'])-max(a['x'],b['x'])>eps and min(a['y']+a['w'],b['y']+b['w'])-max(a['y'],b['y'])>eps


def _walls(demo, doc, room, level, omit_shared=True):
    x,y,l,w,t,h=room['x'],room['y'],room['l'],room['w'],room['t'],room['h']
    z=wall_z(room,level)
    shapes={
        'Frente':demo.box(l,t,h,x,y,z),
        'Fondo':demo.box(l,t,h,x,y+w-t,z),
        'LateralIzquierdo':demo.box(t,w-2*t,h,x,y+t,z),
        'LateralDerecho':demo.box(t,w-2*t,h,x+l-t,y+t,z),
    }
    # No duplicamos la pared que comunica con la habitacion de origen en planta baja.
    omitted={'derecha':'LateralIzquierdo','izquierda':'LateralDerecho','trasera':'Frente'}.get(room['side']) if level==1 and omit_shared else None
    for side, shape in shapes.items():
        if side==omitted: continue
        demo.feature(doc,wall_name(room['idx'],level,side),
                     f'{room["label"]} - {REV[side]} - planta {level}',shape,(.91,.84,.70))


def _cut_passage(demo,doc,parent,room):
    """Abertura de comunicacion en el muro existente, 900 x 2100 mm."""
    side={'derecha':'LateralDerecho','izquierda':'LateralIzquierdo','trasera':'Fondo'}[room['side']]
    target=room_wall(doc,parent,1,side)
    if target is None:
        raise ValueError('No hay pared exterior disponible para comunicar la nueva habitacion.')
    t=parent['t']; z=parent['slab']; h=parent['h']
    if h<2200: raise ValueError('Las paredes son demasiado bajas para la puerta comunicante.')
    if side=='Fondo':
        overlap_from=max(parent['x'],room['x'])
        overlap_to=min(parent['x']+parent['l'],room['x']+room['l'])
        if overlap_to-overlap_from<1300:raise ValueError('No hay espacio suficiente en la pared trasera.')
        cx=(overlap_from+overlap_to)/2
        cutter=demo.box(900,t+20,2100,cx-450,parent['y']+parent['w']-t-10,z)
    else:
        overlap_from=max(parent['y'],room['y'])
        overlap_to=min(parent['y']+parent['w'],room['y']+room['w'])
        if overlap_to-overlap_from<1300:raise ValueError('No hay espacio suficiente en la pared lateral.')
        cy=(overlap_from+overlap_to)/2
        xx=parent['x']+parent['l']-t if side=='LateralDerecho' else parent['x']
        cutter=demo.box(t+20,900,2100,xx-10,cy-450,z)
    demo.cut_opening(target,cutter)


def _create_room(demo,doc,parent,dirn,l,w):
    if not 2000<=l<=12000 or not 2000<=w<=12000:
        raise ValueError('La habitacion debe medir entre 2 y 12 metros por lado.')
    catalog=module_catalog(doc,demo)
    x,y=_module_position(parent,dirn,l,w)
    num=max(catalog)+1
    room={'idx':num,'x':x,'y':y,'l':l,'w':w,'slab':parent['slab'],
          'h':parent['h'],'t':parent['t'],'side':dirn,'parent':parent['idx'],
          'label':f'habitacion {dirn} {num}'}
    if any(_overlap(room,other) for other in catalog.values()):
        raise ValueError('La habitacion se superpone con otra. Elegi otro lado o dimensiones.')
    if parent['h']<=0:raise ValueError('Primero crea las paredes de la habitacion principal.')
    if walls_level(doc,parent)<1: raise ValueError('Primero crea las paredes de la habitacion origen.')
    if not room_wall(doc,parent,1,{'derecha':'LateralDerecho','izquierda':'LateralIzquierdo','trasera':'Fondo'}[dirn]):
        raise ValueError('Ese sector no tiene pared exterior para comunicar las habitaciones.')
    def action():
        obj=demo.feature(doc,floor_name(num),f'Habitacion {dirn} {num}',
                         demo.box(l,w,parent['slab'],x,y,0),(.65,.65,.61))
        for attr,val in [('ModuloX',x),('ModuloY',y),('ModuloLargo',l),('ModuloFondo',w),
                         ('ModuloEspesor',parent['t']),('ModuloAltura',parent['h']),('ModuloLosa',parent['slab'])]:
            obj.addProperty('App::PropertyLength',attr,'Habitacion');setattr(obj,attr,val)
        obj.addProperty('App::PropertyString','ModuloOrigen','Habitacion');obj.ModuloOrigen=str(parent['idx'])
        obj.addProperty('App::PropertyString','ModuloTipo','Habitacion');obj.ModuloTipo=dirn
        # Pared lateral compartida y paso entre habitaciones; no tocamos otras plantas.
        _cut_passage(demo,doc,parent,room)
        _walls(demo,doc,room,1)
    demo.mutate(doc,'Agregar habitacion',action)
    return room


def _room_slab(demo,doc,room):
    level=walls_level(doc,room)+1
    name=slab_name(room['idx'],level)
    if doc.getObject(name):return False,level
    z=top_z(room,level-1)
    demo.mutate(doc,'Entrepiso habitacion',lambda:demo.feature(doc,name,
       f'Entrepiso {room["label"]} nivel {level}',demo.box(room['l'],room['w'],200,room['x'],room['y'],z),(.67,.68,.69)))
    return True,level


def _room_walls(demo,doc,room):
    level=walls_level(doc,room)+1
    if doc.getObject(slab_name(room['idx'],level)) is None:
        raise ValueError('Primero deci crear entrepiso para esta habitacion.')
    demo.mutate(doc,'Paredes habitacion',lambda:_walls(demo,doc,room,level,omit_shared=False))
    return level


def room_roofs(doc,room):
    return [o for o in doc.Objects if o.Name.startswith(roof_prefix(room['idx']))]


def _room_roof(demo,doc,room,kind):
    import math
    import Part
    from FreeCAD import Vector
    level=walls_level(doc,room)
    keys=['Frente','Fondo','LateralIzquierdo','LateralDerecho']
    present=[room_wall(doc,room,level,s) for s in keys]
    if not any(present):raise ValueError('No hay paredes en esta habitacion.')
    eave=max(o.Shape.BoundBox.ZMax for o in present if o)
    x,y,l,w,t=room['x'],room['y'],room['l'],room['w'],room['t']
    def make():
        for ob in list(room_roofs(doc,room)):doc.removeObject(ob.Name)
        base=roof_prefix(room['idx'])
        if kind=='flat':
            demo.feature(doc,base+'Plano',f'Techo plano de {room["label"]} nivel {level}',
                         demo.box(l,w,200,x,y,eave),(.67,.68,.69))
        else:
            # Cubierta con dos faldones y pequeñas salientes; la cumbrera corre en Y.
            pitch=math.tan(math.radians(30))
            center=x+l/2
            ridge=eave+l/2*pitch
            outer=eave-200*pitch
            def prism(coords):
                pts=[Vector(xx,y-200,zz) for xx,zz in coords]
                return Part.Face(Part.makePolygon(pts+[pts[0]])).extrude(Vector(0,w+400,0))
            a=[(x-200,outer),(center,ridge),(center,ridge+120),(x-200,outer+120)]
            b=[(center,ridge),(x+l+200,outer),(x+l+200,outer+120),(center,ridge+120)]
            for key,poly in [('Izquierdo',a),('Derecho',b)]:
                demo.feature(doc,base+key,f'Techo {key} de {room["label"]} nivel {level}',
                             prism(poly),(.65,.17,.10))
    demo.mutate(doc,'Techo de habitacion',make)
    return level


def _room_window(demo,doc,room,level,side):
    wall=room_wall(doc,room,level,side)
    if wall is None:
        raise ValueError('Esa pared es compartida o no existe. Elegi otra pared.')
    num=room['idx']; unique=prefix(num)+f'VentanaNivel{level}{side}'
    if doc.getObject(unique):raise ValueError('Ya existe una ventana en esa pared y planta.')
    x,y,l,w,t=room['x'],room['y'],room['l'],room['w'],room['t']
    z=wall_z(room,level)+1050; ww=700.;wh=950.
    if room['h']<wh+1050:raise ValueError('La pared no es lo suficientemente alta.')
    if side in ('Frente','Fondo'):
        start=x+l/2-ww/2; off=y if side=='Frente' else y+w-t
        hole=demo.box(ww,t+20,wh,start,off-10,z)
        B=lambda along,inset,height,width,depth,high:demo.box(width,depth,high,along,inset,height)
        base=off+25
    else:
        start=y+w/2-ww/2; off=x if side=='LateralIzquierdo' else x+l-t
        hole=demo.box(t+20,ww,wh,off-10,start,z)
        B=lambda along,inset,height,width,depth,high:demo.box(depth,width,high,inset,along,height)
        base=off+25
    def draw():
        demo.cut_opening(wall,hole)
        b=55.;d=55.
        frame=B(start,base,z,ww,d,b)
        frame=frame.fuse(B(start,base,z+wh-b,ww,d,b))
        frame=frame.fuse(B(start,base,z+b,b,d,wh-2*b))
        frame=frame.fuse(B(start+ww-b,base,z+b,b,d,wh-2*b))
        demo.feature(doc,unique,f'Ventana {REV[side]} {room["label"]} nivel {level}',frame.removeSplitter(),(.96,.96,.93))
        glass=demo.feature(doc,unique+'Vidrio',f'Vidrio {REV[side]} {room["label"]} nivel {level}',
                           B(start+b,base+21,z+b,ww-2*b,12,wh-2*b),(.38,.72,.93))
        glass.ViewObject.Transparency=60
    demo.mutate(doc,'Ventana habitacion',draw)


# Seleccion por sector y planta, sin depender del orden de objetos de FreeCAD.
LEVEL_WORDS = {
    'planta baja': 1, 'primer piso': 1, 'primera planta': 1,
    'segundo piso': 2, 'segunda planta': 2, 'planta alta': 2,
    'tercer piso': 3, 'tercera planta': 3,
    'cuarto piso': 4, 'cuarta planta': 4,
    'quinto piso': 5, 'sexta planta': 6, 'sexto piso': 6,
    'septimo piso': 7, 'octavo piso': 8, 'noveno piso': 9,
    'decimo piso': 10, 'ultimo piso': -1, 'ultima planta': -1,
}


def level_label(level):
    return {1:'planta baja',2:'segundo piso',3:'tercer piso',4:'cuarto piso',
            5:'quinto piso',6:'sexto piso'}.get(level, f'nivel {level}')


def room_path(rooms, room_idx):
    """Ruta relativa: 'trasera izquierda' para un anexo izquierdo del trasero."""
    parts=[]
    seen=set()
    while room_idx != 0 and room_idx in rooms and room_idx not in seen:
        seen.add(room_idx)
        room=rooms[room_idx]
        parts.append(room['side'])
        room_idx=room['parent']
    return ' '.join(reversed(parts))


def resolve_room_level(rooms, text, *, default_level=None):
    """Resuelve nombres, rutas anidadas, ID y planta, sin elegir ambiguos."""
    key=norm(text)
    for start in ('seleccionar habitacion ', 'seleccionar ', 'habitacion '):
        if key.startswith(start):
            key=key[len(start):]
            break
    level=default_level
    for phrase, value in sorted(LEVEL_WORDS.items(), key=lambda t:-len(t[0])):
        if key.endswith(' '+phrase):
            key=key[:-(len(phrase)+1)].strip()
            level=value
            break
    m=re.search(r'\s+nivel\s+(\d+)$',key)
    if m:
        level=int(m.group(1)); key=key[:m.start()].strip()
    from demo_house import NUMBERS
    room_id=None
    if key in ('principal','casa principal','central','casa','habitacion principal'):
        room_id=0
    elif key in NUMBERS:
        room_id=NUMBERS[key]
    elif key.isdigit():
        room_id=int(key)
    elif key.startswith('numero ') and key[7:].isdigit():
        room_id=int(key[7:])
    else:
        matches=[n for n,r in rooms.items() if n!=0 and
                 key in (r['side'],r['label'],r['label'].removeprefix('habitacion '),room_path(rooms,n))]
        if len(matches)>1:
            raise ValueError('Hay varias habitaciones con ese nombre. Deci la ruta completa, como trasera izquierda, o el numero de habitacion.')
        if matches: room_id=matches[0]
    if room_id not in rooms:
        raise ValueError('No encontre esa habitacion. Deci ver habitaciones para conocer los nombres.')
    room=rooms[room_id]
    return room_id, level


def focus_room_level(doc, room, level):
    """Resalta un objeto representativo sin seleccionar todos los muros."""
    import FreeCADGui as Gui
    obj=next((room_wall(doc,room,level,side) for side in
              ('Frente','Fondo','LateralDerecho','LateralIzquierdo')
              if room_wall(doc,room,level,side) is not None),None)
    if obj is None and level==1:
        obj=doc.getObject('CasaPiso' if room['idx']==0 else floor_name(room['idx']))
    if obj is not None:
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(obj)
    return obj


def install_room_functions(demo):
    if getattr(demo,'_room_features_installed',False):return demo
    demo._room_features_installed=True
    old_handle=demo.handle
    old_grammar=demo.grammar
    old_answer=demo.answer
    demo._active_room=0
    demo._active_level=None
    demo._room_doc=None
    demo._room_values={}

    def catalog():
        doc,floor=demo.current()
        if demo._room_doc!=doc.Name:
            demo._room_doc=doc.Name
            demo._active_room=0
            demo._active_level=None
        return doc,floor,module_catalog(doc,demo)

    def active():
        doc,floor,rooms=catalog()
        if demo._active_room not in rooms: demo._active_room=0
        return doc,floor,rooms[demo._active_room]

    def choose_room(text):
        doc,floor,rooms=catalog()
        n,requested_level=resolve_room_level(rooms,text)
        room=rooms[n]
        maximum=walls_level(doc,room)
        level=maximum if requested_level in (None,-1) else requested_level
        if level<1 or level>maximum:
            raise ValueError(f'{room["label"]} solo tiene {maximum} piso(s); no existe el nivel {level}.')
        demo._active_room=n
        demo._active_level=level if requested_level is not None else None
        focus_room_level(doc,room,level)
        return demo.tell(f'Seleccionada {room["label"]}, {level_label(level)}. '
                         + ('El techo ira en este nivel.' if requested_level is not None else 'El techo ira en el ultimo nivel.'))

    def grammar():
        p=set(old_grammar())|set(ROOM_CMDS)|set(ROOF_ACTIONS)|set(OTHER)|set(DIRECTIONS)|set(SIDES)
        p.update(('habitacion principal','principal','frontal','trasera','izquierda','derecha',
                  'planta baja','ultimo piso','seleccionar habitacion principal',
                  'seleccionar habitacion derecha','seleccionar habitacion izquierda',
                  'seleccionar habitacion trasera','seleccionar habitacion trasera izquierda',
                  'poner techo a dos aguas','levantar siguiente piso'))
        from demo_house import NUMBERS
        for word, number in NUMBERS.items():
            if 1<=number<=50:
                p.add('seleccionar habitacion '+word);p.add('habitacion '+word)
        short_levels=('planta baja','segundo piso','tercer piso','cuarto piso','ultimo piso')
        for i in range(1,21):
            for key in (str(i),'numero '+str(i)):
                p.add('seleccionar habitacion '+key)
                for suffix in short_levels:
                    p.add('seleccionar habitacion '+key+' '+suffix)
        # Nombres compuestos y nivel: se generan hasta tres habitaciones encadenadas.
        paths={'principal'}
        sides=('derecha','izquierda','trasera')
        for a in sides:
            paths.add(a)
            for b in sides:
                paths.add(a+' '+b)
                for c in sides:
                    paths.add(a+' '+b+' '+c)
        for path in paths:
            p.add('seleccionar habitacion '+path)
            p.add('seleccionar '+path)
            for suffix in short_levels:
                p.add('seleccionar habitacion '+path+' '+suffix)
                p.add('seleccionar '+path+' '+suffix)
        return sorted(p)

    def answer(value):
        stage=demo.pending
        if stage=='room_length':
            demo._room_values['l']=value
            return demo.ask('room_width','¿Que profundidad tendra la nueva habitacion? Por ejemplo cuatro metros.')
        if stage=='room_width':
            v=demo._room_values
            doc,floor,rooms=catalog()
            if doc.Name!=v['document']:raise ValueError('El documento de la casa cambio.')
            parent=rooms.get(v['parent'])
            if parent is None:raise ValueError('No encuentro la habitacion de origen.')
            room=_create_room(demo,doc,parent,v['direction'],v['l'],value)
            demo._active_room=room['idx']
            demo._active_level=None
            demo.pending=None
            demo._room_values={}
            return demo.tell(f'Lista {room["label"]}. Quedo seleccionada. Podes agregar entrepiso, ventana o techo.')
        return old_answer(value)

    def handle(phrase):
        def start_room(direction):
            doc,floor,room=active()
            demo._room_values={'document':doc.Name,'parent':room['idx'],'direction':direction}
            return demo.ask('room_length',f'¿Que largo tendra la nueva habitacion hacia {direction}? Por ejemplo tres metros.')

        p=norm(phrase)
        if demo.pending or demo.prompt:
            return old_handle(phrase)
        if p.startswith('seleccionar habitacion ') and p not in ROOM_CMDS:
            return choose_room(p)
        if p.startswith('seleccionar ') and p not in ROOM_CMDS:
            candidate=p.removeprefix('seleccionar ')
            if candidate.startswith(('principal','trasera','derecha','izquierda','habitacion ')):
                return choose_room(p)
        if p=='ver habitaciones' or p=='listar habitaciones':
            doc,floor,rooms=catalog()
            names=', '.join(r['label'] + ' (ruta: ' + (room_path(rooms,n) or 'principal') + ', '+str(walls_level(doc,r))+' pisos)' for n,r in rooms.items())
            return demo.tell('Habitaciones disponibles: '+names+'. Seleccionada '+rooms[demo._active_room]['label']+'.')
        if p=='ayuda habitaciones':
            return demo.tell('Agregar habitacion derecha, izquierda o trasera; seleccionar habitacion; crear entrepiso; levantar siguiente piso; poner ventana; poner techo plano o a dos aguas; quitar techo; ver habitaciones; guardar casa.')
        if p in ROOM_CMDS:
            kind=ROOM_CMDS[p]
            if kind == 'add_prompt':
                doc, _, _ = active()

                def add_at(direction):
                    demo.showcase.require_active(doc)
                    return start_room(direction)

                return demo.ask_options('room_side', '¿Hacia dónde querés ampliar?', DIRECTIONS, add_at)
            if kind == 'choose':
                doc, _, rooms = catalog()
                from demo_house import NUMBERS

                aliases = {}
                labels = {}
                for idx, room in rooms.items():
                    path = room_path(rooms, idx) or 'principal'
                    candidates = {path, room['side'] or 'principal', room['label'], str(idx), f'numero {idx}'}
                    candidates.update(word for word, number in NUMBERS.items() if number == idx)
                    maximum = walls_level(doc, room)
                    for candidate in sorted(candidates):
                        for suffix in ('', *LEVEL_WORDS):
                            phrase = (candidate + ' ' + suffix).strip()
                            try:
                                key = resolve_room_level(rooms, phrase)
                            except ValueError:
                                continue
                            level = key[1]
                            if key[0] != idx or (level is not None and level > maximum):
                                continue
                            aliases[phrase] = key
                            aliases['habitacion ' + phrase] = key
                            label = room['label'].capitalize()
                            labels[key] = label if level is None else f'{label} — {level_label(maximum if level == -1 else level)}'

                def select(key):
                    demo.showcase.require_active(doc)
                    room, level = key
                    suffix = '' if level is None else ' ultimo piso' if level == -1 else f' nivel {level}'
                    return choose_room(f'{room}{suffix}')

                return demo.ask_options('select_room', '¿Qué habitación querés seleccionar?', aliases, select, labels)
            if kind=='main':return choose_room('principal')
            if kind.startswith('add_'):
                return start_room({'add_right':'derecha','add_left':'izquierda','add_back':'trasera'}[kind])
        if p in ROOF_SHORT and demo.showcase.active_facade():
            return demo.showcase.handle(p)
        if p in WINDOW_3D:
            import FreeCAD as App
            doc = App.ActiveDocument
            if doc is None or doc.getObject('CasaPiso') is None:
                return demo.showcase.window_choice()

        # En la casa principal delegamos al modo previo, manteniendo compatibilidad.
        doc,floor,room=active() if p in ROOF_ACTIONS or p in OTHER else (None,None,None)
        if room is None:
            return old_handle(phrase)
        # Casa principal: no se permite un techo entre plantas ya construidas.
        if room['idx']==0:
            if p in ROOF_ACTIONS and demo._active_level not in (None,walls_level(doc,room)):
                raise ValueError('La casa principal tiene paredes encima de esa planta. Selecciona ultimo piso para colocar el techo.')
            if p in ROOF_SHORT:
                return old_handle('poner techo a dos aguas')
            if p in WINDOW_3D:
                if walls_level(doc, room) == 1:
                    return demo.showcase.window_choice()
                return old_handle('poner ventana')
            return old_handle(phrase)
        if p in OTHER:
            kind=OTHER[p]
            if kind == 'window':
                from demo_extension import ask_level

                def choose_wall(side):
                    demo.showcase.require_active(doc)

                    def place(level):
                        demo.showcase.require_active(doc)
                        _room_window(demo, doc, room, level, side)
                        demo.tell(f'Ventana creada en {room["label"]}, nivel {level}.')

                    maximum = walls_level(doc, room)
                    if maximum == 1:
                        return place(1)
                    return ask_level(demo, maximum, place)

                return demo.ask_options('room_window_wall', '¿En qué pared de la habitación va la ventana?',
                                        SIDES, choose_wall)
            if kind=='slab':
                if room_roofs(doc,room):raise ValueError('Primero deci quitar techo en esta habitacion.')
                created,n=_room_slab(demo,doc,room)
                return demo.tell('Entrepiso nivel '+str(n)+' listo.' if created else 'Ya existe ese entrepiso. Deci levantar siguiente piso.')
            if kind=='walls':
                if room_roofs(doc,room):raise ValueError('Primero deci quitar techo en esta habitacion.')
                n=_room_walls(demo,doc,room)
                return demo.tell(f'Paredes del nivel {n} listas en {room["label"]}.')
            if kind in ('remove','hide','show'):
                roofs=room_roofs(doc,room)
                if not roofs:return demo.tell('Esta habitacion no tiene techo.')
                if kind=='remove':
                    demo.mutate(doc,'Quitar techo habitacion',lambda:[doc.removeObject(ob.Name) for ob in list(roofs)])
                    return demo.tell('Techo quitado de '+room['label']+'.')
                for ob in roofs:ob.ViewObject.Visibility=(kind=='show')
                return demo.tell('Techo visible.' if kind=='show' else 'Techo oculto.')
        if p in ROOF_ACTIONS:
            max_level=walls_level(doc,room)
            if demo._active_level is not None and demo._active_level != max_level:
                raise ValueError(f'{room["label"]} tiene paredes hasta el nivel {max_level}. Para evitar que el techo atraviese otra planta, selecciona ultimo piso.')
            n=_room_roof(demo,doc,room,ROOF_ACTIONS[p])
            return demo.tell(f'Techo en {room["label"]}, sobre el nivel {n}.')
        return old_handle(phrase)

    demo.grammar=grammar
    demo.answer=answer
    demo.handle=handle
    return demo
