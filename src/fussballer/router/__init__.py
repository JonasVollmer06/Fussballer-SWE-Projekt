# Copyright (C) 2023 - present Juergen Zimmermann, Hochschule Karlsruhe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Modul für die REST-Schnittstelle einschließlich Validierung."""

from collections.abc import Sequence

from fussballer.router.fussballer_router import fussballer_router, get_by_id
from fussballer.router.fussballer_router_helloworld import (
    fussballer_router_hello_world,
    test,
)

__all__: Sequence[str] = [
    "fussballer_router",
    "fussballer_router_hello_world",
    "get_by_id",
    "test",
]
