from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Set, Dict


# -----------------------------
# Dominio organizacional
# -----------------------------

@dataclass(frozen=True)
class Holding:
    id: str
    nombre: str


@dataclass(frozen=True)
class Empresa:
    id: str
    nombre: str
    holding_id: str


@dataclass(frozen=True)
class Area:
    id: str
    nombre: str
    empresa_id: str
    holding_id: str  # redundante a propósito para validar rápido y evitar joins mentales


# -----------------------------
# Usuarios y roles
# -----------------------------

class Rol(str, Enum):
    INVERSIONISTA = "INVERSIONISTA"
    GERENTE = "GERENTE"
    JEFATURA = "JEFATURA"
    TRABAJADOR = "TRABAJADOR"


@dataclass
class Usuario:
    id: str
    nombre: str
    rol: Rol

    # Alcances de gestión (no de lectura):
    holding_ids: Set[str] = field(default_factory=set)   # por si algún rol gestiona holdings
    empresa_ids: Set[str] = field(default_factory=set)   # inversionista gestiona varias empresas
    area_ids: Set[str] = field(default_factory=set)      # gerente gestiona varias áreas

    def can_manage_empresa(self, empresa: Empresa) -> bool:
        if self.rol == Rol.INVERSIONISTA:
            return empresa.id in self.empresa_ids
        # si quisieras permitir otros roles, se agrega acá
        return False

    def can_manage_area(self, area: Area) -> bool:
        if self.rol == Rol.GERENTE:
            return area.id in self.area_ids
        if self.rol in (Rol.JEFATURA, Rol.TRABAJADOR):
            # normalmente empleados no "gestionan áreas" salvo que quieras permitirlo
            return False
        return False


# -----------------------------
# Documentos y permisos
# -----------------------------

class Scope(str, Enum):
    PERSONA = "PERSONA"
    AREA = "AREA"
    EMPRESA = "EMPRESA"
    HOLDING = "HOLDING"


@dataclass(frozen=True)
class ShareRule:
    """
    Una regla de visibilidad:
    - scope=HOLDING target_id=holding_id  => visible para autorizados dentro del holding
    - scope=EMPRESA  target_id=empresa_id  => visible para autorizados dentro de esa empresa
    - scope=AREA     target_id=area_id     => visible para autorizados dentro de esa área
    - scope=PERSONA  target_id=user_id     => visible solo para esa persona
    """
    scope: Scope
    target_id: str


@dataclass
class Documento:
    id: str
    titulo: str
    creado_por_user_id: str

    # Documento puede estar en varias áreas (y por lo tanto varias empresas),
    # pero deben ser del mismo holding.
    area_ids: Set[str] = field(default_factory=set)

    # Reglas de visibilidad por nivel
    share_rules: Set[ShareRule] = field(default_factory=set)

    # Opcional: owners o “personas asociadas” (distinto a share)
    owners_user_ids: Set[str] = field(default_factory=set)

    def attach_area(self, area: Area, areas_index: Dict[str, Area]) -> None:
        """
        Adjunta un área, validando que todas las áreas del doc pertenezcan al mismo holding.
        """
        if not self.area_ids:
            self.area_ids.add(area.id)
            return

        existing_holding = areas_index[next(iter(self.area_ids))].holding_id
        if area.holding_id != existing_holding:
            raise ValueError(
                f"Documento no puede cruzar holdings. "
                f"Existente={existing_holding}, Nueva={area.holding_id}"
            )
        self.area_ids.add(area.id)

    def share_to_holding(self, holding_id: str) -> None:
        self.share_rules.add(ShareRule(Scope.HOLDING, holding_id))

    def share_to_empresa(self, empresa_id: str) -> None:
        self.share_rules.add(ShareRule(Scope.EMPRESA, empresa_id))

    def share_to_area(self, area_id: str) -> None:
        self.share_rules.add(ShareRule(Scope.AREA, area_id))

    def share_to_persona(self, user_id: str) -> None:
        self.share_rules.add(ShareRule(Scope.PERSONA, user_id))


# -----------------------------
# Autorización de lectura
# -----------------------------

def can_view_document(
    user: Usuario,
    doc: Documento,
    *,
    holdings: Dict[str, Holding],
    empresas: Dict[str, Empresa],
    areas: Dict[str, Area],
    miembros_area: Dict[str, Set[str]],     # area_id -> set(user_id)
    miembros_empresa: Dict[str, Set[str]],  # empresa_id -> set(user_id)
    miembros_holding: Dict[str, Set[str]],  # holding_id -> set(user_id)
) -> bool:
    # 1) El creador siempre ve
    if user.id == doc.creado_por_user_id:
        return True

    # 2) Owners (si usás este concepto) siempre ven
    if user.id in doc.owners_user_ids:
        return True

    # 3) Reglas PERSONA
    if ShareRule(Scope.PERSONA, user.id) in doc.share_rules:
        return True

    # 4) Reglas AREA (si el usuario pertenece a esa área)
    for rule in doc.share_rules:
        if rule.scope == Scope.AREA:
            if user.id in miembros_area.get(rule.target_id, set()):
                return True

    # 5) Reglas EMPRESA (si el usuario pertenece a esa empresa)
    for rule in doc.share_rules:
        if rule.scope == Scope.EMPRESA:
            if user.id in miembros_empresa.get(rule.target_id, set()):
                return True

    # 6) Reglas HOLDING (si el usuario pertenece a ese holding)
    for rule in doc.share_rules:
        if rule.scope == Scope.HOLDING:
            if user.id in miembros_holding.get(rule.target_id, set()):
                return True

    # 7) Si no hay share_rules, podrías decidir:
    # - privado por defecto (False)  ✅ (lo más seguro)
    return False


# -----------------------------
# Autorización de "gestión" (compartir / modificar permisos)
# -----------------------------

def can_manage_document(user: Usuario, doc: Documento) -> bool:
    """
    Quién puede cambiar permisos del documento.
    Regla base: creador o jefatura (según tu negocio).
    """
    if user.id == doc.creado_por_user_id:
        return True
    if user.rol == Rol.JEFATURA:
        return True
    return False


# -----------------------------
# Ejemplo de uso mínimo
# -----------------------------
if __name__ == "__main__":
    h1 = Holding("H1", "Holding Uno")
    e1 = Empresa("E1", "Empresa Uno", "H1")
    e2 = Empresa("E2", "Empresa Dos", "H1")

    a1 = Area("A1", "Área Finanzas", "E1", "H1")
    a2 = Area("A2", "Área TI", "E2", "H1")

    holdings = {h1.id: h1}
    empresas = {e1.id: e1, e2.id: e2}
    areas = {a1.id: a1, a2.id: a2}

    u_trab = Usuario("U1", "Ana", Rol.TRABAJADOR)
    u_ger  = Usuario("U2", "Luis", Rol.GERENTE, area_ids={"A1", "A2"})
    u_inv  = Usuario("U3", "Sol", Rol.INVERSIONISTA, empresa_ids={"E1", "E2"})

    miembros_area = {"A1": {"U1", "U2"}, "A2": {"U2"}}
    miembros_empresa = {"E1": {"U1", "U2", "U3"}, "E2": {"U2", "U3"}}
    miembros_holding = {"H1": {"U1", "U2", "U3"}}

    doc = Documento("D1", "Reporte Q1", creado_por_user_id="U1")
    doc.attach_area(a1, areas)
    doc.attach_area(a2, areas)  # permitido: mismo holding H1

    # Compartir a nivel empresa E1 (por ejemplo)
    doc.share_to_empresa("E1")

    print("Trabajador ve?:", can_view_document(u_trab, doc,
        holdings=holdings, empresas=empresas, areas=areas,
        miembros_area=miembros_area, miembros_empresa=miembros_empresa, miembros_holding=miembros_holding
    ))
    print("Gerente ve?:", can_view_document(u_ger, doc,
        holdings=holdings, empresas=empresas, areas=areas,
        miembros_area=miembros_area, miembros_empresa=miembros_empresa, miembros_holding=miembros_holding
    ))
    print("Inversionista ve?:", can_view_document(u_inv, doc,
        holdings=holdings, empresas=empresas, areas=areas,
        miembros_area=miembros_area, miembros_empresa=miembros_empresa, miembros_holding=miembros_holding
    ))
