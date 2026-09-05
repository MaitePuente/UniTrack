from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytest

from app.domain.materia import EstadoMateria, Materia, PeriodoMateria


def crear_materia(**cambios: object) -> Materia:
    datos: dict[str, object] = {
        "nombre": "Programación I",
        "anio_carrera": 1,
        "periodo": PeriodoMateria.PRIMER_CUATRIMESTRE,
    }
    datos.update(cambios)
    return Materia(**datos)  # type: ignore[arg-type]


def test_crear_materia_con_valores_predeterminados() -> None:
    materia = crear_materia(nombre="  Programación I  ")

    assert isinstance(materia.id, UUID)
    assert materia.nombre == "Programación I"
    assert materia.estado is EstadoMateria.PENDIENTE
    assert materia.color == "#7567c8"
    assert materia.creada_en.utcoffset() is not None
    assert materia.modificada_en.utcoffset() is not None


def test_rechaza_id_que_no_sea_uuid() -> None:
    with pytest.raises(TypeError, match="id debe ser un UUID"):
        crear_materia(id="no-es-un-uuid")


@pytest.mark.parametrize("nombre", ["", "   "])
def test_rechaza_nombre_vacio(nombre: str) -> None:
    with pytest.raises(ValueError, match="nombre no puede estar vacío"):
        crear_materia(nombre=nombre)


@pytest.mark.parametrize("nombre", [None, 42])
def test_rechaza_nombre_con_tipo_incorrecto(nombre: object) -> None:
    with pytest.raises(TypeError, match="nombre debe ser un string"):
        crear_materia(nombre=nombre)


@pytest.mark.parametrize("anio_carrera", [0, -1])
def test_rechaza_anio_no_positivo(anio_carrera: int) -> None:
    with pytest.raises(ValueError, match="anio_carrera debe ser positivo"):
        crear_materia(anio_carrera=anio_carrera)


@pytest.mark.parametrize("anio_carrera", [True, 1.5, "1"])
def test_rechaza_anio_con_tipo_incorrecto(anio_carrera: object) -> None:
    with pytest.raises(TypeError, match="anio_carrera debe ser un entero"):
        crear_materia(anio_carrera=anio_carrera)


@pytest.mark.parametrize(
    ("campo", "valor", "mensaje"),
    [
        ("periodo", "anual", "periodo debe ser un PeriodoMateria"),
        ("estado", "pendiente", "estado debe ser un EstadoMateria"),
    ],
)
def test_periodo_y_estado_exigen_enums(
    campo: str, valor: object, mensaje: str
) -> None:
    with pytest.raises(TypeError, match=mensaje):
        crear_materia(**{campo: valor})


def test_normaliza_color() -> None:
    materia = crear_materia(color="  violeta  ")

    assert materia.color == "violeta"


@pytest.mark.parametrize("color", ["", "   "])
def test_rechaza_color_vacio(color: str) -> None:
    with pytest.raises(ValueError, match="color no puede estar vacío"):
        crear_materia(color=color)


def test_rechaza_color_con_tipo_incorrecto() -> None:
    with pytest.raises(TypeError, match="color debe ser un string"):
        crear_materia(color=None)


@pytest.mark.parametrize("campo", ["creada_en", "modificada_en"])
def test_rechaza_fechas_sin_zona_horaria(campo: str) -> None:
    with pytest.raises(ValueError, match=f"{campo} debe incluir zona horaria"):
        crear_materia(**{campo: datetime(2026, 9, 3, 12, 0)})


@pytest.mark.parametrize("campo", ["creada_en", "modificada_en"])
def test_rechaza_fechas_con_tipo_incorrecto(campo: str) -> None:
    with pytest.raises(TypeError, match=f"{campo} debe ser un datetime"):
        crear_materia(**{campo: "2026-09-03"})


def test_rechaza_modificacion_anterior_a_creacion() -> None:
    creada_en = datetime(2026, 9, 3, 12, 0, tzinfo=timezone.utc)

    with pytest.raises(
        ValueError, match="modificada_en no puede ser anterior a creada_en"
    ):
        crear_materia(
            creada_en=creada_en,
            modificada_en=creada_en - timedelta(seconds=1),
        )
