# c-org - Command line tools to manage Continuous Organisations


# Website

https://c-org.co



# Installation

You need `Python > 3.5.3` because `web3.py` is using `typing`. If you are using an older version of Python, you can use `pyenv` to install a new one. In this case, make sure you activate the virtual environment each time you are using `c-org`.

```bash
# install pyenv
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
# install python 3.6.5
pyenv install 3.6.5
# create a virtual environment
pyenv virtualenv 3.6.5 c-org
# activate it
pyenv activate c-org
```


Then, you can easily install `c-org` with the following commands:

```bash
pip install .
python -m solc.install v0.4.24

# For running tests, you need a local provider:
# First on a separate terminal, install and run ganache-cli
# then in the repository, run
python -m unittest discover
```

# Using `c-org`

The continuous organisation is built inside a separate folder.

1. Create a `params.yaml` as given in [example](../master/configs/example.yaml) or run `c-org init`.

2. Create a wallet containing enough gas to deploy the continuous organisation on the ethereum net.

```bash
c-org wallet create my_wallet
```

The wallet is store locally and you can re-use it.

3. Deploy the continuous organisation :

```bash
c-org deploy params.yaml
```

Several files are generated in `$HOME/.c-org/my-c-org/`, but you can set the destination path with the `--destination` argument.

4. Finally, you can buy, sell, add revenues ou see statistics with the commands:

```bash
c-org {buy, sell, revenue, stats} --help
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
