# c-org

![c-org status](https://img.shields.io/badge/status-alpha-yellow.svg)
[![Twitter URL](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/ContinuousOrg)

`c-org` is the command line tool used to create and interact with Continuous Organizations


# About Continuous Organizations

To learn more about Continuous Organizations, please visit: https://c-org.co


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
sudo add-apt-repository ppa:ethereum/ethereum # requires python-software-properties installed
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
```

Finally, on a separate terminal, run `py.test`:

```bash
cd /path/to/c-org/
py.test
```

The tests suite is launching `ganache-cli`, but you might want to launch it by yourself if you want to check your Continuous Organisation before launching it on `mainnet`.

# Using `c-org`

The continuous organisation called `NAME` is built inside a separate folder. By default, this folder is `DIRECTORY = $HOME/.c-org/NAME`.

1. Create a `config.yaml` as given in [example](../master/example.yaml) or run `c-org init` to generate one.

2. Create a wallet containing enough gas to deploy the continuous organisation on the ethereum blockchain. Please note that this wallet is the admin wallet, used to deploy the smart-contract, it is **not** the wallet of the Continuous Organization (which is specified in the config.yaml file).

```bash
c-org wallet create NAME
```

The wallet is stored locally and you can re-use it. Add some ethers to it. If you're using ganache, you can use Metamask set on the localhost network to do that. Otherwise, use your favorite wallet to transfer some ethers (~ 0.1 eth) to it.

3. Deploy the continuous organisation:

```bash
c-org deploy /path/to/config.yaml [--wallet NAME]
```


4. Finally, you can buy, sell, add revenues ou see statistics with the commands:

```bash
c-org {buy, sell, revenue, stats} --help
```

# TODO


* **Node provider**. Everything was tested with `ganache`. Adding `infura` and local ethereum node support is necessary. Similarly, automated tests should use `testrpc` instead of depending on an extern call to `ganache`.
* **Wallet**. The local admin wallet creation process is highly insecure right now. Level 0 (minimum) is to encrypt it with a user provided passphrase. Then, using the ethereum-go API to support using an already created local wallet would be great. In the future (once WalletConnect is functional), implementing a command-line version of WalletConnect to allow users to securely use their favorite wallet would be ideal.
* **Documentation**. As the API is not stable yet, the documentation is not written. Instead, the user should use `--help` argument.
* **Versioning**. I am wondering how to deal with change in a smart contract, such as it would break the API. I am considering for now a factory pattern to instance the API corresponding to the version.
* **Generating static files**. A user interface is required to burn/mint tokens. User interfaces will be developed in separated repository and a link to this repository will be given as a parameter in `params.yaml`.
