import os.path

from matplotlib import pyplot as plt
from oemof import solph


def PrintResults(output, dumpfile):
    if dumpfile is not None:
        energysystem = solph.EnergySystem()
        energysystem.restore(dpath=os.path.dirname(dumpfile), filename=os.path.basename(dumpfile))

    output_str = ""

    # define an alias for shorter calls below (optional)
    results = energysystem.results["main"]
    storage = energysystem.groups["storage"]

    # print a time slice of the state of charge
    output_str += "********* State of Charge (slice) *********" + "\n"
    data = results[(storage, None)]["sequences"]["2022-01-01 01:00:00":"2022-01-14 00:00:00"]

    output_str += data.to_string(header=True, index=True) + "\n"
    output_str += "********* Main results *********" + "\n"

    # get all variables of a specific component/bus
    custom_storage = solph.views.node(results, "storage")
    electricity_bus = solph.views.node(results, "electricity")
    pp_gas = solph.views.node(results, "pp_gas")
    excess_bel = solph.views.node(results, "excess_bel")

    busses = []

    for nodename in energysystem.groups:
        if isinstance(energysystem.groups[nodename], solph.Bus):
            busses.append(energysystem.groups[nodename])

    for bus in busses:
        data = solph.views.node(results, bus.label)
        keys = data.keys()

        if "sequences" in keys:
            for value in data["sequences"].sum(axis=0):
                output_str += str(value) + "\n"
        elif "scalars" in keys:
            output_str += bus["scalars"]

    if not os.path.exists(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output))

    if os.path.exists(output):
        os.remove(output)

    xfile = open(os.path.join(output), 'wt')
    xfile.write(output_str)
    xfile.close()

    # plot the time series (sequences) of a specific component/bus
    if plt is not None:
        fig, axs = plt.subplots(nrows=4, ncols=1, sharex='all', figsize=(8, 11))
        ax11, ax12, ax13, ax14 = axs

        custom_storage["sequences"].plot(
            fig=fig, ax=ax11, kind="line", drawstyle="steps-post", title="Speicher"
        )

        excess_bel["sequences"].plot(
            fig=fig, ax=ax12, kind="line", drawstyle="steps-post", title="Überschüssiger Strom"
        )

        pp_gas["sequences"].plot(
            fig=fig, ax=ax13, kind="line", drawstyle="steps-post", title="Transformator Gas > Strom"
        )

        electricity_bus["sequences"].plot(
            fig=fig, ax=ax14, kind="line", drawstyle="steps-post", title="Strombus"
        )

        for ax in axs:
            ax.legend(bbox_to_anchor=(1, 1), loc="upper left", fontsize="8")

        plt.tight_layout()
        # plt.show()

        plotdir = os.path.join(os.getcwd(), "images")
        if not os.path.exists(plotdir):
            os.makedirs(plotdir)

        plt.savefig(fname=os.path.join(plotdir, os.path.basename(output) + ".pdf"),
                    format="pdf",
                    dpi=None,
                    facecolor='w',
                    edgecolor='w',
                    transparent=False,
                    bbox_inches=None,
                    pad_inches=0.1)
