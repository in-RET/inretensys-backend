from gurobipy import GRB
from InRetEnsys.common.log import InRetEnsysLogger


# Define my callback function
def persistentSolverCallback(cb_m, cb_opt, cb_where):
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
        InRetEnsysLogger.info("Simplex...")

    elif cb_where == GRB.Callback.MIP:
        # General MIP callback
        what = 0

        if what == 0:
            InRetEnsysLogger.info('NoRel Heuristic Phase - MIP General')
        elif what == 1:
            InRetEnsysLogger.info('Standard MIP Search - MIP General')
        elif what == 2:
            InRetEnsysLogger.info('Solution Improvement - MIP General')

    elif cb_where == GRB.Callback.MIPSOL:
        # MIP solution callback
        InRetEnsysLogger.info('MIP Solution Callback -> hier müsste dann eine Ausgabe passieren, ob abgebrochen werden soll.')
        cb_opt.terminate()

    elif cb_where == GRB.Callback.MIPNODE:
        # MIP node callback
        InRetEnsysLogger.info('MIP Node Callback')

    elif cb_where == GRB.Callback.BARRIER:
        # Barrier callback
        InRetEnsysLogger.info('Barrier Callback')

    elif cb_where == GRB.Callback.MESSAGE:
        # Message callback
        msg = cb_opt.cbGet(GRB.Callback.MSG_STRING)
        #logger.info(msg)


# Define my callback function
def SolverCallback(model, where):
    if where == GRB.Callback.POLLING:
        # Ignore polling callback
        #logger.info("Polling...")
        pass

    elif where == GRB.Callback.PRESOLVE:
        # Ignore Presolve callback
        #logger.info("Presolve...")
        pass 

    elif where == GRB.Callback.SIMPLEX:
        # Simplex callback
        InRetEnsysLogger.info("Simplex...")

    elif where == GRB.Callback.MIP:
        # General MIP callback

        what = model.cbGet(GRB.Callback.MIP_PHASE)

        if what == GRB.PHASE_MIP_SEARCH:
            InRetEnsysLogger.info('NoRel Heuristic Phase - MIP General')
        elif what == 1:
            InRetEnsysLogger.warn('Standard MIP Search - MIP General')
        elif what == 2:
            InRetEnsysLogger.warn('Solution Improvement - MIP General')

    elif where == GRB.Callback.MIPSOL:
        # MIP solution callback
        InRetEnsysLogger.info('MIP Solution Callback -> hier müsste dann eine Ausgabe passieren, ob abgebrochen werden soll.')
        model.terminate()

    elif where == GRB.Callback.MIPNODE:
        # MIP node callback
        InRetEnsysLogger.info('MIP Node Callback')

    elif where == GRB.Callback.BARRIER:
        # Barrier callback
        InRetEnsysLogger.info('Barrier Callback')

    elif where == GRB.Callback.MESSAGE:
        # Message callback
        msg = model.cbGet(GRB.Callback.MSG_STRING)
        #InRetEnsysLogger.info(msg)