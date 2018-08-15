## Introduction
Continuous Organisations are a new way to think about equities.
This utility aims at creating such organizations.

The organizations must be described in separated YAML files inside the folder `c-orgs/`.
The command `derive create` will then create each Continuous Organisation whose `deployed` flag is equal to false.

## General structure
Continuous organisations' configuration files use the
[YAML](<http://yaml.org/spec/1.1/current.html>) format.

The top-level node in a configuration file is a ``c-org:`` mapping
that contains the version of the smart contract (currently ``version: 0.1``),  the `deployed` flag, the parameters, the addresses and the type of `node-provider`.

## Full example

```yaml
  version: 0.1
  deployed: false
  parameters:
    slope: 1.0
    alpha: 0.1
    beta: 0.3
  addresses:
    smart-contract: ~
    owner: ~
  name: my_continuous_organisation
```
