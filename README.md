# InRetEnsys
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/c8a4262a7fe54ec2b1499943226b1708)](https://app.codacy.com/gh/in-RET/inretensys-backend/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/c8a4262a7fe54ec2b1499943226b1708)](https://app.codacy.com/gh/in-RET/inretensys-backend/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)

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


