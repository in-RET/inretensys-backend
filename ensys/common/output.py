import os.path

from matplotlib import pyplot as plt
from oemof import solph


def SearchNode(nodeslist, nodename):
    for node in nodeslist:
        if node.label == nodename:
            return nodeslist[nodeslist.index(node)]

    return None


def PrintResultsFromDump(dumpfile, output):
    # ****************************************************************************
    # ********** PART 2 - Processing the results *********************************
    # ****************************************************************************
    energysystem = solph.EnergySystem()
    energysystem.restore(dpath=os.path.dirname(dumpfile), filename=os.path.basename(dumpfile))

    # define an alias for shorter calls below (optional)
    results = energysystem.results["main"]
    storage = energysystem.groups["storage"]

    bel = SearchNode(energysystem.nodes, "electricity")
    pp_gas = SearchNode(energysystem.nodes, "pp_gas")

    if os.path.exists(output):
        os.remove(output)

    xfile = open(os.path.join(output), 'at')

    # print a time slice of the state of charge
    print("********* State of Charge (slice) *********", file=xfile)
    #"2012-02-25 08:00:00": "2012-02-26 15:00:00"
    print(results[(storage, None)]["sequences"]["2022-01-01 01:00:00":"2022-01-14 00:00:00"], file=xfile)

    # get all variables of a specific component/bus
    custom_storage = solph.views.node(results, "storage")
    electricity_bus = solph.views.node(results, "electricity")
    pp_gas = solph.views.node(results, "pp_gas")
    excess_bel = solph.views.node(results, "excess_bel")
    natural_gas_bus = solph.views.node(results, "natural_gas")

    # plot the time series (sequences) of a specific component/bus
    if plt is not None:
        fig, axs = plt.subplots(nrows=4, ncols=1, sharex='all', figsize=(8, 11))
        ax11, ax12, ax13, ax14 = axs

        custom_storage["sequences"].plot(
            ax=ax11, kind="line", drawstyle="steps-post", title="Speicher"
        )

        excess_bel["sequences"].plot(
            ax=ax12, kind="line", drawstyle="steps-post", title="Überschüssiger Strom"
        )

        pp_gas["sequences"].plot(
            ax=ax13, kind="line", drawstyle="steps-post", title="Transformator Gas > Strom"
        )

        electricity_bus["sequences"].plot(
            ax=ax14, kind="line", drawstyle="steps-post", title="Strombus"
        )

        for ax in axs:
            ax.legend(bbox_to_anchor=(1, 1), loc="upper left", fontsize="8")

        plt.tight_layout()
        plt.show()

    # print the solver results
    #print("********* Meta results *********", file=xfile)
    # Meta results are others for every system e.g. wallclocktime
    #print(energysystem.results["meta"], file=xfile)

    # print the sums of the flows around the electricity bus
    print("********* Main results *********", file=xfile)
    print(electricity_bus["sequences"].sum(axis=0), file=xfile)

    if True is True:
        my_results = electricity_bus["scalars"]

        # installed capacity of storage in GWh
        my_results["storage_invest_GWh"] = (
                results[(storage, None)]["scalars"]["invest"] / 1e6
        )

        print(my_results, file=xfile)

    if True is False:
        my_results = natural_gas_bus["scalars"]

        # installed capacity of storage in GWh
        my_results["gas_invest_GWh"] = (
                results[(pp_gas, bel)]["scalars"]["invest"] / 1e6
        )

        print(my_results, file=xfile)

    xfile.close()





