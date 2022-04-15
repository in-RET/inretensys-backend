import pprint as pp

from matplotlib import pyplot as plt
from oemof import solph


def PrintResultsFromDump(dpath, dumpfile):
    # ****************************************************************************
    # ********** PART 2 - Processing the results *********************************
    # ****************************************************************************
    energysystem = solph.EnergySystem()
    energysystem.restore(dpath=dpath, filename=dumpfile)

    # define an alias for shorter calls below (optional)
    results = energysystem.results["main"]
    storage = energysystem.groups["storage"]

    # print a time slice of the state of charge
    print("")
    print("********* State of Charge (slice) *********")
    print(results[(storage, None)]["sequences"]["2012-02-25 08:00:00":"2012-02-26 15:00:00"])
    print("")

    # get all variables of a specific component/bus
    custom_storage = solph.views.node(results, "storage")
    electricity_bus = solph.views.node(results, "electricity")

    # plot the time series (sequences) of a specific component/bus
    if plt is not None:
        fig, ax = plt.subplots(figsize=(10, 5))
        custom_storage["sequences"].plot(
            ax=ax, kind="line", drawstyle="steps-post"
        )
        plt.legend(
            loc="upper center",
            prop={"size": 8},
            bbox_to_anchor=(0.5, 1.25),
            ncol=2,
        )
        fig.subplots_adjust(top=0.8)
        plt.show()

        fig, ax = plt.subplots(figsize=(10, 5))
        electricity_bus["sequences"].plot(
            ax=ax, kind="line", drawstyle="steps-post"
        )
        plt.legend(
            loc="upper center", prop={"size": 8}, bbox_to_anchor=(0.5, 1.3), ncol=2
        )
        fig.subplots_adjust(top=0.8)
        plt.show()

    # print the solver results
    print("********* Meta results *********")
    pp.pprint(energysystem.results["meta"])
    print("")

    # print the sums of the flows around the electricity bus
    print("********* Main results *********")
    print(electricity_bus["sequences"].sum(axis=0))
