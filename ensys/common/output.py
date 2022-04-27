import os.path

from matplotlib import pyplot as plt
from oemof import solph


def PrintResultsFromDump(dumpfile, output):
    # ****************************************************************************
    # ********** PART 2 - Processing the results *********************************
    # ****************************************************************************
    energysystem = solph.EnergySystem()
    energysystem.restore(dpath=os.path.dirname(dumpfile), filename=os.path.basename(dumpfile))

    # define an alias for shorter calls below (optional)
    results = energysystem.results["main"]
    storage = energysystem.groups["storage"]

    if os.path.exists(output):
        os.remove(output)

    xfile = open(os.path.join(output), 'at')

    # print a time slice of the state of charge
    print("********* State of Charge (slice) *********", file=xfile)
    print(results[(storage, None)]["sequences"]["2012-02-25 08:00:00":"2012-02-26 15:00:00"], file=xfile)

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
    print("********* Meta results *********", file=xfile)
    # Meta results are others for every system e.g. wallclocktime
    #print(energysystem.results["meta"], file=xfile)

    # print the sums of the flows around the electricity bus
    print("********* Main results *********", file=xfile)
    print(electricity_bus["sequences"].sum(axis=0), file=xfile)

    xfile.close()





