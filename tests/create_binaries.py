import os

import configs.ENSYS.basic_sample
import configs.ENSYS.allround1_sample
import configs.ENSYS.allround2_sample
import configs.ENSYS.allround3_sample
import configs.ENSYS.SWE2021_V08_O4_2045_BEW0_S1_Geoth_Wind


def createBinaries():
    datadir = os.path.join(os.getcwd(), "configs", "DATEN", "SWE Test")
    print(datadir)

    configs.ENSYS.basic_sample.CreateConfiguration()
    configs.ENSYS.allround1_sample.CreateConfiguration()
    configs.ENSYS.allround2_sample.CreateConfiguration()
    configs.ENSYS.allround3_sample.CreateConfiguration()
    configs.ENSYS.SWE2021_V08_O4_2045_BEW0_S1_Geoth_Wind.CreateConfiguration(datadir)


createBinaries()
