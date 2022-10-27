from gurobipy import GRB
from InRetEnsys.common.log import InRetEnsysLogger


# Define my callback function
def SolverCallback(cb_m, cb_opt, cb_where):
    logger = InRetEnsysLogger("SolverLogger", "/Users/pyrokar/Documents/GitHub/python/inretensys/inretensys-backend/tests/logs/gurobi_callback.log")

    if cb_where == GRB.Callback.POLLING:
        # Ignore polling callback
        #logger.info("Polling...")
        pass

    elif cb_where == GRB.Callback.PRESOLVE:
        # Ignore Presolve callback
        #logger.info("Presolve...")
        pass 

    elif cb_where == GRB.Callback.SIMPLEX:
        # Simplex callback
        logger.info("Simplex...")

    elif cb_where == GRB.Callback.MIP:
        # General MIP callback
        logger.info('General MIP Callback')

    elif cb_where == GRB.Callback.MIPSOL:
        # MIP solution callback
        logger.info('MIP Solution Callback -> hier müsste dann eine Ausgabe passieren, ob abgebrochen werden soll.')

    elif cb_where == GRB.Callback.MIPNODE:
        # MIP node callback
        logger.info('MIP Node Callback')

    elif cb_where == GRB.Callback.BARRIER:
        # Barrier callback
        logger.info('Barrier Callback')

    elif cb_where == GRB.Callback.MESSAGE:
        # Message callback
        msg = cb_opt.cbGet(GRB.Callback.MSG_STRING)
        #logger.info(msg)