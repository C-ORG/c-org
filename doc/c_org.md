## Introduction
Continuous Organisations are a new way to think about equities.
This utility aims at creating such organizations.

The organization must be described in a YAML file.
The command `c_org deploy /path/to/yaml` will then create the Continuous Organisation.

## General structure
Continuous organisations' configuration files use the
[YAML](<http://yaml.org/spec/1.1/current.html>) format.

The top-level node in a configuration file is a ``c-org:`` mapping
that contains the version of the smart contract (currently ``version: 0.1``), the parameters, the addresses.

## Full example

```yaml
manifest_version: 0.1 # the version of this manifest format
c-org:
  name: 'Decusis' # the name of your continuous organization
  summary: 'The 1st continuous organization' # summary of your organization (optional)
  website: 'https://invest.decusis.com' # website where users can get interact with your continuous organization (optional)
  wallet: '0x3aebb26a66b328cd8a60415710ce4de147657b0b' # main wallet of the organization
  token_units: 1000000 # the larger, the smaller the nominal value of your token (keep default if in doubt)
  investor_reserve: 10% # percentage of invested money put in reserve
  revenue_reserve: 30% # percentage of revenues put in reserve
  initial_tokens: 1000000 # the number of tokens initially availabl
```
