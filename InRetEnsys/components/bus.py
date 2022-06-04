from oemof import solph

from InRetEnsys import InRetEnsysConfigContainer


class InRetInRetEnsysBus(InRetEnsysConfigContainer):
    label: str
    balanced: bool = True

    def to_oemof(self, energysystem: solph.EnergySystem) -> solph.Bus:
        """
        Return an oemof-object build with the args of the object.
        :return: oemof-bus-object
        :rtype: solph.Bus
        :param energysystem: the oemof-energysystem to build the kwargs of the object
        :type energysystem: solph.Energysystem
        """
        kwargs = self.build_kwargs(energysystem)

        return solph.Bus(**kwargs)
