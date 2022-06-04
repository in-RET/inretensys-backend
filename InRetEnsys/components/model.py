from pydantic import validator

from InRetEnsys import InRetEnsysConfigContainer, InRetEnsysEnergysystem
from InRetEnsys.types import Solver


class InRetEnsysModel(InRetEnsysConfigContainer):
    energysystem: InRetEnsysEnergysystem
    solver: Solver = Solver.gurobi
    solver_verbose: bool = True

    @classmethod
    @validator('energysystem')
    def es_is_not_none(cls, v):
        if v is None:
            raise ValueError("Energysystem can not be 'None'.")

        return v