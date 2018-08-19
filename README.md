# derive - Command line tools to derive Continuous Organisations


# Website

https://c-org.co

# Documentation

The full documentation for `derive` is available in the [doc/derive.md file](../master/doc/derive.md)



# Installation


```bash
pip install .
python -m solc.install v0.4.24
```

# Use

```bash
c_org derive --name my_continuous_organisation
c_org {buy, sell, revenue, stats} --help
```

# TODO list

## Include wallets

For now, the addresses are just randomly picked from the node provider.

## Node provider

Everything was tested with `ganache`. Including `infura` and testing on real blockchains is necessary. Similarly, automated tests should use `testrpc` instead of depending on an extern call to `ganache`.

## Installation

Installation is quite basic for now and it does not check for python version, solc and other dependencies.

## Documentation

As the API is not stable yet, the documentation is not written. Instead, the user should use `--help` argument.

## Versioning

I am wondering how to deal with change in a smart contract, such as it would break the API. I am considering for now a factory pattern to instance the API corresponding to the version.

## Generating static files

A user interface is required to burn/mint tokens. A library should be generated with the ABI and the address of the smart contract. 
