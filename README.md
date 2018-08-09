# lazyTickets

A script to generate scrum tickets from a backlog

# Usage

I assume you already have a backlog with the correct format. 

First you need to export this `backlog.numbers` into csv files

Then you you must simply run 
```bash
lazytickets -s S1 -f backlog.csv
```

 - `-s` option must match the sprint tag you want to export. It is used in the first coloumn of the backlog.
 - `-f` option indicates the csv file to parse
 - `--singleTaskStories` option indicates that you want to print tasks for stories with only one task #DEPRECATED
 - `--no-singleTaskStories`  option indicates that you don't want to print tasks for stories with only one task, instead, the task TAG is added to the story **(Default behavior)** #DEPRECATED

 
The output files will be `tickets_i.jpg` and will be placed on the folder you executed the script.

# Backlog format
Backlog sheet : 

| field  |  column |
|:-:|:-:|
| Sprint | A |
| Scenario  | D |
| En tant que  | E |
| Je veux  | F |
| Afin de  | G |
| Priorité  |  H |
| Points  | I |

Tasks sheet : 

| field  |  column |
|:-:|:-:|
| Sprint | A |
| Scenario  | D |
| Tag  |  E |
| Description  |  F |
| Estimated  |  H |

# Setup
This is a python script, it can be installed with pip 
Install from git : `pip3 install git+git://github.com/aardouin/lazytickets.git`

Download the latest release at https://github.com/aardouin/lazyTickets/releases/
and perform 
`pip3 install [path_to_tar.gz]`


# Development 
In order to generate the release file `python3 setup.py sdist`
Please not that version is located in `setup.py`
