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

You also need to [install `solc`](https://solidity.readthedocs.io/en/v0.4.24/installing-solidity.html) to compile Solidity smart contract:
```bash
# On Ubuntu:
sudo add-apt-repository ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install solc

# On other Linux distros:
sudo snap install solc

# On macOS:
brew update
brew upgrade
brew tap ethereum/ethereum
brew install solidity
```


Then, you can easily install `c-org` with the following command (make sure you have the latest version of pip installed):

```bash
pip install -e .
```

# Testing

For running tests, you need a local provider. First, download and install [node.js](https://nodejs.org/en/). Then install and run `ganache-cli`:

```bash
npm install -g ganache-cli
ganache-cli
```

Finally, on a separate terminal, run `py.test`:

```bash
cd /path/to/c-org/
py.test
```

# Using `c-org`

The continuous organisation called `NAME` is built inside a separate folder. By default, this folder is `DIRECTORY = $HOME/.c-org/NAME`.

1. Create a `config.yaml` as given in [example](../master/example.yaml) or run `c-org init` to generate one.

2. Create a wallet containing enough gas to deploy the continuous organisation on the ethereum net.

```bash
c-org wallet create NAME
```

The wallet is store locally and you can re-use it. Add some ethers on it. For example, you can use [Metamask](https://medium.com/verasity/how-to-transfer-ethereum-to-metamask-wallet-security-67ff0a415c88) for that.

3. Deploy the continuous organisation :

```bash
c-org deploy /path/to/config.yaml [--wallet NAME]
```


4. Finally, you can buy, sell, add revenues ou see statistics with the commands:

```bash
c-org {buy, sell, revenue, stats} --help
```

# TODO list


## Node provider

Everything was tested with `ganache`. Adding `infura` and testing on real blockchains is necessary. Similarly, automated tests should use `testrpc` instead of depending on an extern call to `ganache`.

## Documentation

As the API is not stable yet, the documentation is not written. Instead, the user should use `--help` argument.

## Versioning

I am wondering how to deal with change in a smart contract, such as it would break the API. I am considering for now a factory pattern to instance the API corresponding to the version.

## Generating static files

A user interface is required to burn/mint tokens. User interfaces will be developed in separated repository and a link to this repository will be given as a parameter in `params.yaml`.
