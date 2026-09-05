from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4


class EstadoMateria(StrEnum):
    PENDIENTE = "pendiente"
    CURSANDO = "cursando"
    REGULARIZADA = "regularizada"
    APROBADA = "aprobada"


class PeriodoMateria(StrEnum):
    ANUAL = "anual"
    PRIMER_CUATRIMESTRE = "primer_cuatrimestre"
    SEGUNDO_CUATRIMESTRE = "segundo_cuatrimestre"


def _ahora_utc() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(kw_only=True)
class Materia:
    nombre: str
    anio_carrera: int
    periodo: PeriodoMateria
    id: UUID = field(default_factory=uuid4)
    estado: EstadoMateria = EstadoMateria.PENDIENTE
    color: str = "#7567c8"
    creada_en: datetime = field(default_factory=_ahora_utc)
    modificada_en: datetime = field(default_factory=_ahora_utc)

    def __post_init__(self) -> None:
        if not isinstance(self.id, UUID):
            raise TypeError("id debe ser un UUID")

        if not isinstance(self.nombre, str):
            raise TypeError("nombre debe ser un string")
        self.nombre = self.nombre.strip()
        if not self.nombre:
            raise ValueError("nombre no puede estar vacío")

        if isinstance(self.anio_carrera, bool) or not isinstance(self.anio_carrera, int):
            raise TypeError("anio_carrera debe ser un entero")
        if self.anio_carrera <= 0:
            raise ValueError("anio_carrera debe ser positivo")

        if not isinstance(self.periodo, PeriodoMateria):
            raise TypeError("periodo debe ser un PeriodoMateria")
        if not isinstance(self.estado, EstadoMateria):
            raise TypeError("estado debe ser un EstadoMateria")

        if not isinstance(self.color, str):
            raise TypeError("color debe ser un string")
        self.color = self.color.strip()
        if not self.color:
            raise ValueError("color no puede estar vacío")

        self._validar_fecha_con_zona(self.creada_en, "creada_en")
        self._validar_fecha_con_zona(self.modificada_en, "modificada_en")
        if self.modificada_en < self.creada_en:
            raise ValueError("modificada_en no puede ser anterior a creada_en")

    @staticmethod
    def _validar_fecha_con_zona(fecha: datetime, campo: str) -> None:
        if not isinstance(fecha, datetime):
            raise TypeError(f"{campo} debe ser un datetime")
        if fecha.tzinfo is None or fecha.utcoffset() is None:
            raise ValueError(f"{campo} debe incluir zona horaria")
