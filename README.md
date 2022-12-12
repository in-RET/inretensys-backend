# InRetEnsys
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/415669eb789c42208e2d76489b3e826f)](https://www.codacy.com/gh/pyrokar1993/hsn.oemof.web.configurator/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=pyrokar1993/hsn.oemof.web.configurator&amp;utm_campaign=Badge_Grade)

Package to Map oemof.solph-Classes to abstract classes for further use.

## Usage
This package comes with an CLI-Interface to start and simulate energymodels. 

### Configuration
To configurate an energymodel use therefore the following classes. Beginning with the components and adding them afterwards to an energysystem and energymodel.

Possible Classes:
- InRetEnsysBus
- InRetEnsysSink
- InRetEnsysSource
- InRetEnsysTransformer
- InRetEnsysStorage
- InRetEnsysEnergysystem
- InRetEnsysModel

### External Start
To start the application it is necessary to define the following classes (and dump them into a file):
- InRetEnsysModel
- InRetEnsysEnergysystem

```bash
python main.py [-olp] [-wdir WORKINGDIRECTORY] configfile
```
#### Parameters:

olp - It's a flag to select the single output of the lp-File
wdir - Path to the Workingdirectory, if not given it's the current directory

configfile - Necessary - the path to the configuration which is build before (binary or json)


