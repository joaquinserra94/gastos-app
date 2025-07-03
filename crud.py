from sqlalchemy.orm import Session
import models

def crear_grupo(db: Session, grupo):
    db_grupo = models.Grupo(nombre=grupo.nombre)
    db.add(db_grupo)
    db.commit()
    db.refresh(db_grupo)
    return db_grupo

def obtener_grupos(db: Session):
    return db.query(models.Grupo).all()

def crear_persona(db: Session, persona):
    db_persona = models.Persona(nombre=persona.nombre, grupo_id=persona.grupo_id)
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona

def crear_gasto(db: Session, gasto):
    db_gasto = models.Gasto(
        descripcion=gasto.descripcion,
        monto=gasto.monto,
        pagador_id=gasto.pagador_id,
        grupo_id=gasto.grupo_id
    )
    db.add(db_gasto)
    db.commit()
    db.refresh(db_gasto)
    return db_gasto

def obtener_gastos_por_grupo(db: Session, grupo_id: int):
    return db.query(models.Gasto).filter(models.Gasto.grupo_id == grupo_id).all()

def calcular_resumen_grupo(db: Session, grupo_id: int):
    grupo = db.query(models.Grupo).filter(models.Grupo.id == grupo_id).first()
    if not grupo:
        return {"error": "Grupo no encontrado"}

    personas = grupo.personas
    gastos = grupo.gastos

    if not personas or not gastos:
        return {"mensaje": "Aún no hay suficientes datos para calcular"}

    # Total gastado por cada persona
    total_por_persona = {p.id: 0 for p in personas}
    for gasto in gastos:
        total_por_persona[gasto.pagador_id] += gasto.monto

    # Gasto total y gasto promedio por persona
    gasto_total = sum(g.monto for g in gastos)
    n = len(personas)
    promedio = gasto_total / n

    # Cuánto debe o le deben a cada persona
    balance = {p.id: total_por_persona[p.id] - promedio for p in personas}

    # Armar resumen de deudas
    resumen = []

    deudores = [p.id for p in personas if balance[p.id] < 0]
    acreedores = [p.id for p in personas if balance[p.id] > 0]

    deudores.sort(key=lambda pid: balance[pid])
    acreedores.sort(key=lambda pid: balance[pid], reverse=True)

    id_to_nombre = {p.id: p.nombre for p in personas}

    i, j = 0, 0
    while i < len(deudores) and j < len(acreedores):
        deudor = deudores[i]
        acreedor = acreedores[j]
        deuda = min(-balance[deudor], balance[acreedor])

        resumen.append({
            "deudor": id_to_nombre[deudor],
            "acreedor": id_to_nombre[acreedor],
            "monto": round(deuda, 2)
        })

        balance[deudor] += deuda
        balance[acreedor] -= deuda

        if balance[deudor] == 0:
            i += 1
        if balance[acreedor] == 0:
            j += 1

    return resumen

def resumen_individual(db: Session, grupo_id: int):
    grupo = db.query(models.Grupo).filter(models.Grupo.id == grupo_id).first()
    if not grupo:
        return {"error": "Grupo no encontrado"}

    personas = grupo.personas
    gastos = grupo.gastos

    if not personas or not gastos:
        return {"mensaje": "Aún no hay suficientes datos para calcular"}

    total_por_persona = {p.id: 0 for p in personas}
    for gasto in gastos:
        total_por_persona[gasto.pagador_id] += gasto.monto

    gasto_total = sum(g.monto for g in gastos)
    n = len(personas)
    promedio = gasto_total / n

    resumen = []
    for persona in personas:
        gasto_real = total_por_persona[persona.id]
        balance = round(gasto_real - promedio, 2)

        resumen.append({
            "persona": persona.nombre,
            "gasto_total": round(gasto_real, 2),
            "gasto_promedio": round(promedio, 2),
            "balance": balance
        })

    return resumen

def calcular_liquidacion(db: Session, grupo_id: int):
    grupo = db.query(models.Grupo).filter(models.Grupo.id == grupo_id).first()
    if not grupo:
        return {"error": "Grupo no encontrado"}

    personas = grupo.personas
    gastos = grupo.gastos
    pagos = db.query(models.Pago).filter(models.Pago.grupo_id == grupo_id).all()

    if not personas or not gastos:
        return {"mensaje": "Aún no hay suficientes datos para calcular"}

    total_por_persona = {p.id: 0 for p in personas}
    for gasto in gastos:
        total_por_persona[gasto.pagador_id] += gasto.monto

    gasto_total = sum(g.monto for g in gastos)
    promedio = gasto_total / len(personas)

    # Balance inicial sin pagos
    balance = {p.id: total_por_persona[p.id] - promedio for p in personas}

    # Aplicar pagos: si Ana le pagó 10 a Juan, Ana debe menos y Juan recibe menos
    for pago in pagos:
        balance[pago.deudor_id] += pago.monto
        balance[pago.acreedor_id] -= pago.monto

    id_to_nombre = {p.id: p.nombre for p in personas}

    deudores = sorted([pid for pid in balance if balance[pid] < 0], key=lambda x: balance[x])
    acreedores = sorted([pid for pid in balance if balance[pid] > 0], key=lambda x: -balance[x])

    resumen = []
    i, j = 0, 0
    while i < len(deudores) and j < len(acreedores):
        deudor_id = deudores[i]
        acreedor_id = acreedores[j]

        deuda = min(-balance[deudor_id], balance[acreedor_id])
        deuda = round(deuda, 2)

        if deuda > 0:
            resumen.append({
                "deudor": id_to_nombre[deudor_id],
                "acreedor": id_to_nombre[acreedor_id],
                "monto": deuda
            })

            balance[deudor_id] += deuda
            balance[acreedor_id] -= deuda

        if abs(balance[deudor_id]) < 0.01:
            i += 1
        if abs(balance[acreedor_id]) < 0.01:
            j += 1

    return resumen


def registrar_pago(db: Session, pago):
    nuevo_pago = models.Pago(
        deudor_id=pago.deudor_id,
        acreedor_id=pago.acreedor_id,
        grupo_id=pago.grupo_id,
        monto=pago.monto
    )
    db.add(nuevo_pago)
    db.commit()
    db.refresh(nuevo_pago)
    return nuevo_pago

def obtener_pagos(db: Session, grupo_id: int):
    return db.query(models.Pago).filter(models.Pago.grupo_id == grupo_id).all()

def editar_grupo(db: Session, grupo_id: int, nuevo_nombre: str):
    grupo = db.query(models.Grupo).filter(models.Grupo.id == grupo_id).first()
    if grupo:
        grupo.nombre = nuevo_nombre
        db.commit()
        db.refresh(grupo)
    return grupo

def editar_persona(db: Session, persona_id: int, nuevo_nombre: str):
    persona = db.query(models.Persona).filter(models.Persona.id == persona_id).first()
    if persona:
        persona.nombre = nuevo_nombre
        db.commit()
        db.refresh(persona)
    return persona


