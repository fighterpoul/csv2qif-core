# About
`csv2qif` is a simple command line script written in Python that helps you converting list of transactions exported from your bank in `csv` format into `qif` file that may be used in programs like HomeBank.

# Installation
I recommend using `conda`, here are the steps:

1. Clone this repo: `git clone <url>`
1. Enter the folder: `cd csv2qif-core`
1. Create a conda environment: `conda env create -f environment.yml`
1. Activate the environment: `conda activate csv2qif`
1. Install script and plugins you need: `python setup.py install`
1. Check if it works: 
```shell script
> csv2qif --help
> csv2qif-plugins
```
    

# Usages
```shell script
> csv2qif --help
Usage: csv2qif [OPTIONS] CSV_FILE [list of available plugins] OUTPUT_QIF_FILE

Options:
  -a, --account-name    TEXT
  --help                Show this message and exit.
```

Example:
```shell script
> csv2qif transactions.csv ing transactions.qif
```

# Plugins
Script knows how to convert input `csv` file into output `qif` file because of the selected plugin, which is responsible for this part of job.

###Listing available plugins
```
> csv2qif-plugins 
ing, mbank, millennium
```

### Where can I find those plugins?
1. [ING](https://github.com/fighterpoul/csv2qif-ing)
2. [mBank](https://github.com/fighterpoul/csv2qif-mbank)
3. [Millennium](https://github.com/fighterpoul/csv2qif-millennium)

### How can I write my own plugin? I can't see my bank on the list above.
It's really simple - plugin is a single Python file with the logic. I propose you to check one of the available plugins, adapt the file with the plugin's code to your needs, install your new plugin and run it.