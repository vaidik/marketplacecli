Marketplace CLI
===============

Get some everyday work done on Marketplace.

## Installation

```
pip install -e git+https://github.com/vaidik/Marketplace.Python.git@0.0.1#egg=Marketplace
git clone https://github.com/vaidik/marketplacecli.git
cd marketplacecli
python setup.py install
```

## Configuration

`marketplacecli` requires OAuth tokens to communicate with the API. You may
put them in a file called `marketplacecli.yml` either in your working
directory or in your home directory. You may also use the `--config` argument
to provide the path of the config file everytime you run `marketplacecli`.

**Note**:  `marketplacecli.yml` follows [YAML][Y] format.

A [sample configuration][mc] has been provided in the repository which you may copy
to your home directory or working directory.

[mc]: https://github.com/vaidik/marketplacecli/blob/master/marketplacecli.yml
[Y]: http://en.wikipedia.org/wiki/YAML

## Usage

```
# to create 1 app for all the tiers, do:
marketplacecli create_apps

# to do the same thing as we did with previous command but on stage
marketplacecli --env stage create_apps

# to do the same thing as we did with previous command but on prod
marketplacecli --env prod create_apps
```

## Arguments

Coming soon.
