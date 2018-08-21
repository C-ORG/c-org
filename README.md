# c_org - Command line tools to derive Continuous Organisations


# Website

https://c-org.co



# Installation

You need `Python > 3.5.3` because `web3.py` is using `typing`. If you are using an older version of Python, you can use `pyenv` to install a new one. In this case, make sure you activate the virtual environment each time you are using `c_org`.

```bash
# install pyenv
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
# install python 3.6.5
pyenv install 3.6.5
# create a virtual environment
pyenv virtualenv 3.6.5 corg
# activate it
pyenv activate corg
```


Then, you can easily install `c_org` with the following commands:

```bash
pip install .
python -m solc.install v0.4.24

# For running tests, you need a local provider:
# First on a separate terminal, install and run ganache-cli
# then in the repository, run
python -m unittest discover
```

# Use

The continuous organisation is built inside a separate folder.

```bash
c_org init my_continuous_organisation
nano params.yaml
c_org wallet add my_wallet my_private_key
c_org derive
c_org {buy, sell, revenue, stats} --help
```

# TODO list

## Include wallets

For now, the addresses are just randomly picked from the node provider.

## Node provider

Everything was tested with `ganache`. Adding `infura` and testing on real blockchains is necessary. Similarly, automated tests should use `testrpc` instead of depending on an extern call to `ganache`.

## Installation

Installation is quite basic for now and it does not check for python version, solc and other dependencies.

## Documentation

As the API is not stable yet, the documentation is not written. Instead, the user should use `--help` argument.

## Versioning

I am wondering how to deal with change in a smart contract, such as it would break the API. I am considering for now a factory pattern to instance the API corresponding to the version.

## Generating static files

A user interface is required to burn/mint tokens. A library should be generated with the ABI and the address of the smart contract.
