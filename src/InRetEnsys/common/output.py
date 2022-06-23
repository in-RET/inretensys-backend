import os.path

from matplotlib import pyplot as plt
from oemof import solph


def PrintResults(output, dumpfile):
    if dumpfile is not None:
        energysystem = solph.EnergySystem()
        energysystem.restore(dpath=os.path.dirname(dumpfile), filename=os.path.basename(dumpfile))

    # define an alias for shorter calls below (optional)
    results = energysystem.results["main"]
    storage = energysystem.groups["storage"]
    bel = energysystem.groups["electricity"]

    if not os.path.exists(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output))

    if os.path.exists(output):
        os.remove(output)

    xfile = open(os.path.join(output), 'at')

    # print a time slice of the state of charge
    print("********* State of Charge (slice) *********", file=xfile)
    data = results[(storage, None)]["sequences"]["2022-01-01 01:00:00":"2022-01-14 00:00:00"]

    md_data = data.to_string(header=True, index=True)
    print(md_data, file=xfile)

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

        ax11 = custom_storage["sequences"].plot(
            fig=fig, ax=ax11, kind="line", drawstyle="steps-post", title="Speicher"
        )

        ax12 = excess_bel["sequences"].plot(
            fig=fig, ax=ax12, kind="line", drawstyle="steps-post", title="Überschüssiger Strom"
        )

        ax13 = pp_gas["sequences"].plot(
            fig=fig, ax=ax13, kind="line", drawstyle="steps-post", title="Transformator Gas > Strom"
        )

        ax14 = electricity_bus["sequences"].plot(
            fig=fig, ax=ax14, kind="line", drawstyle="steps-post", title="Strombus"
        )

        for ax in axs:
            ax.legend(bbox_to_anchor=(1, 1), loc="upper left", fontsize="8")

        plt.tight_layout()
        # plt.show()

        plotdir = os.path.join(os.getcwd(), "images")
        if not os.path.exists(plotdir):
            os.mkdir(plotdir)

        plt.savefig(fig=fig,
                    ax=axs,
                    fname=os.path.join(plotdir, os.path.basename(output) + ".png"),
                    dpi=None,
                    facecolor='w',
                    edgecolor='w',
                    transparent=False,
                    bbox_inches=None,
                    pad_inches=0.1)

    # print the sums of the flows around the electricity bus
    print("********* Main results *********", file=xfile)
    print(electricity_bus["sequences"].sum(axis=0), file=xfile)

    if "scalars" in electricity_bus.keys():
        my_results = electricity_bus["scalars"]

        # installed capacity of storage in GWh
        my_results["storage_invest_GWh"] = (
                results[(storage, None)]["scalars"]["invest"] / 1e6
        )

        print(my_results, file=xfile)

    if "scalars" in natural_gas_bus.keys():
        my_results = natural_gas_bus["scalars"]

        print(my_results, file=xfile)

    xfile.close()
