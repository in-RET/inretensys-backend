from pydantic import validator

from ensys import EnsysConfigContainer, EnsysEnergysystem
from ensys.types import Solver


class InRetSysModel(EnsysConfigContainer):
    energysystem: EnsysEnergysystem
    solver: Solver = Solver.gurobi
    solver_verbose: bool = True

    @classmethod
    @validator('energysystem')
    def es_is_not_none(cls, v):
        if v is None:
            raise ValueError("Energysystem can not be 'None'.")

        return v