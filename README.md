# lazyTickets

A script to generate scrum tickets from a backlog @ Wopata

# Usage

I assume you already have a backlog with the correct format. 

First you need to export this `backlog.numbers` into csv files

Then you you must simply run 
```bash
lazytickets -s S1 -f backlog
```
 - `-s` option must match the sprint tag you want to export. It is used in the first coloumn of the backlog.
 - `-f` option indicates the folder where the csv export can be found, default is your currentDir
 
 The output files will be `tickets_i.jpg` and will be placed on the folder you executed the script.

# Setup
This is a python script, it can be installed with pip 
Install from git : `pip3 install git+git://github.com/aardouin/lazytickets.git`

Download the latest release at https://github.com/aardouin/lazyTickets/releases/
and perform 
`pip3 install [path_to_tar.gz]`


# Development 
In order to generate the release file `python3 setup.py sdist`
Please not that version is located in `setup.py`