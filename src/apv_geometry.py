"""Geometry helpers for calculating section factor Ap/V for custom profiles."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class ApvGeometryType:
    """A supported profile exposure geometry for Ap/V calculation."""

    key: str
    label: str
    perimeter_mm: Callable[[float, float], float]
    description: str


APV_GEOMETRY_TYPES: tuple[ApvGeometryType, ...] = (
    ApvGeometryType(
        key="freestanding_column",
        label="Fritstående søjle",
        perimeter_mm=lambda a, b: 2 * a + 2 * b,
        description="Alle fire sider er eksponerede: F = 2a + 2b.",
    ),
    ApvGeometryType(
        key="double_column_freestanding",
        label="Dobbeltsøjle, fritstående",
        perimeter_mm=lambda a, b: 4 * a + 2 * b,
        description="Dobbeltsøjle med fri eksponering: F = 4a + 2b.",
    ),
    ApvGeometryType(
        key="column_at_external_wall",
        label="Søjle ved ydervæg",
        perimeter_mm=lambda a, b: a + 2 * b,
        description="Siden mod ydervæggen medregnes ikke: F = a + 2b.",
    ),
    ApvGeometryType(
        key="column_at_corner",
        label="Søjle ved hjørne",
        perimeter_mm=lambda a, b: a + b,
        description="To sider ved hjørnet medregnes ikke: F = a + b.",
    ),
    ApvGeometryType(
        key="beam_under_slab",
        label="Bjælke under dæk",
        perimeter_mm=lambda a, b: a + 2 * b,
        description="Bjælkens underside og to sider er eksponerede: F = a + 2b.",
    ),
    ApvGeometryType(
        key="beam_embedded_in_slab",
        label="Bjælke indlagt i dæk",
        perimeter_mm=lambda a, b: a,
        description="Kun bjælkens underside er eksponeret: F = a.",
    ),
)

APV_GEOMETRY_BY_KEY = {geometry.key: geometry for geometry in APV_GEOMETRY_TYPES}


def calculate_exposed_perimeter_mm(geometry_key: str, a_mm: float, b_mm: float) -> float:
    """Calculate exposed/internal perimeter F in mm for a supported geometry."""

    if a_mm <= 0 or b_mm <= 0:
        raise ValueError("a and b must be greater than 0 mm")

    try:
        geometry = APV_GEOMETRY_BY_KEY[geometry_key]
    except KeyError as exc:
        raise ValueError(f"Unknown Ap/V geometry type: {geometry_key}") from exc

    return geometry.perimeter_mm(a_mm, b_mm)


def calculate_apv_from_geometry(geometry_key: str, a_mm: float, b_mm: float, steel_area_mm2: float) -> float:
    """Calculate Ap/V in m⁻¹ from geometry dimensions and steel area.

    The Fireboard custom-profile flow stores Ap/V in m⁻¹. With F in mm and
    A in mm², Ap/V is calculated as F / A * 1000.
    """

    if steel_area_mm2 <= 0:
        raise ValueError("A must be greater than 0 mm²")

    exposed_perimeter_mm = calculate_exposed_perimeter_mm(geometry_key, a_mm, b_mm)
    return exposed_perimeter_mm / steel_area_mm2 * 1000
