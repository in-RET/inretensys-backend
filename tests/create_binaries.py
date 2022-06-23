import configs.ENSYS.basic_sample
import configs.ENSYS.allround1_sample
import configs.ENSYS.allround2_sample
import configs.ENSYS.allround3_sample


def createBinaries():
    configs.ENSYS.basic_sample.CreateConfiguration()
    configs.ENSYS.allround1_sample.CreateConfiguration()
    configs.ENSYS.allround2_sample.CreateConfiguration()
    configs.ENSYS.allround3_sample.CreateConfiguration()


createBinaries()
