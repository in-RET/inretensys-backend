from pydantic import validator

from InRetEnsys import InRetEnsysConfigContainer, InRetEnsysEnergysystem
from InRetEnsys.types import Solver

##  Container which contains the params for an InRetEnsys-Model
#   
#   @param energysystem The Energysystem which should be optimized.
#   @param solver The Solvername for the optimization.
#   @param solver_verbose Set true if the solver should print his output and steps.
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