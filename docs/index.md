# Ensys
...not Ansys

## What is it?
A python backend script to configure oemof-energysystems from a web interface.
The calculation of the energysystem is possible with an short python-script to build the real oemof-objects and calaculate the model at an high performance center.

Bachlorthesis from Andreas Lubojanski at the University of Applied Science Nordhausen.

Help for future docs:
For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Project layout
The system is configured by a webinterface and these file is dumped to an binary file with all params.
These file is given to an Modelbuilder (see [Modelbuilder](common/modelbuilder.md)) and builds the oemof-objects with the given arguments.
After this step the model is optimised and calculated. 
All results are stored with the model in a given file.

### Ablauf und Aufteilung
```mermaid
sequenceDiagram
  autonumber
  Nutzer->>Webinterface: Erzeugung der Struktur <br> Eingabe des Parametrisierung
  Webinterface->>Nutzer: Ensys-Energysystem als binäre Datei
  Nutzer->>Rechenzentrum: HPC-Parameter <br> Ensys-Konfigurationsdatei
  Rechenzentrum->>Rechenzentrum: Erstellung, Optimierung und <br> Berechnung des Energysystem <br> aus der Konfigurationsdatei
  Rechenzentrum->>Nutzer: Information, die Daten bearbeitet wurden
  Nutzer->>Nutzer: Erstellung der Ausgabe <br> Plots, Datenslices etc.
```

### Klassendiagramm
```mermaid
classDiagram
    direction RL
    class EnsysConfig {
        __init__(self)
        to_oemof(self)
    }

    class EnsysEnergysystem {
        - label: str
        - busses: list of EnsysBus
        - sinks: list of EnsysSink
        - sources: list of EnsysSource
        - transformers: list of EnsysTransformers
        - storages: list of EnsysStorages
        - timeindex: pandas.datetimeindex
        - timeincrement: str
        __init__(self)
    }

    class EnsysBus {
        - label: str
        - balanced: bool
        __init__(self)
        to_oemof(self)
    }

    class EnsysSink {
        - label: str
        - inputs: dicts of EnsysBus.Label: EnsysFlow
        __init__(self)
    }

    class EnsysSource {
        - label: str
        - outputs: dicts of EnsysBus.Label: EnsysFlow
        __init__(self)
    }

    class EnsysStorage {
        - label: str = "Default Storage"
        - inputs: dict
        - outputs: dict
        - nominal_storage_capacity: float
        - invest_relation_input_capacity: float
        - invest_relation_output_capacity: float
        - invest_relation_input_output: float
        - initial_storage_level: float
        - balanced: bool
        - loss_rate: float
        - fixed_losses_relative: float
        - fixed_losses_absolute: float
        - inflow_conversion_factor: float
        - outflow_conversion_factor: float
        - min_storage_level: float
        - max_storage_level: float
        - investment: EnsysInvestment
        __init__(self)
    }

    class EnsysTransformer {
        - label: str
        - inputs: dict
        - outputs: dict
        - conversion_factors: dict
        __init__(self)
    }

    class EnsysInvestment {
        - maximum: float
        - minimum: float
        - ep_costs: float
        - existing: float
        - nonconvex: bool
        - offset: float
        __init__(self)
        to_oemof(self) -> solph.Investment
    }

    class EnsysNonConvex {
        - startup_costs: float
        - shutdown_costs: float
        - activity_costs: float
        - minimum_uptime: int
        - minimum_downtime: int
        - maximum_startups: int
        - maximum_shutdowns: int
        - initial_status: int
        - positive_gradient: dict
        - negative_gradient: dict
        __init__(self)
        to_oemof(self)
    }

    class EnsysFlow {
        - nominal_value: float
        - fix: float
        - min: float
        - max: float
        - positive_gradient: dict
        - negative_gradient: dict
        - summed_max: float
        - summed_min: float
        - variable_costs: float
        - investment: EnsysInvestment
        - nonconvex: EnsysNonConvex
        __init__(self)
        to_oemof(self)
    }

    EnsysConfig <|-- EnsysEnergysystem
    EnsysConfig <|-- EnsysBus
    EnsysConfig <|-- EnsysFlow
    EnsysConfig <|-- EnsysSink
    EnsysConfig <|-- EnsysSource
    EnsysConfig <|-- EnsysStorage
    EnsysConfig <|-- EnsysTransformer
    EnsysConfig <|-- EnsysInvestment
    EnsysConfig <|-- EnsysNonConvex
```

```mermaid
classDiagram
    direction RL

    classA <|-- classB : implements
    classC *-- classD : composition
    classE o-- classF : aggregation
```