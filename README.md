Scripts
=======
Collection of useful scripts



### Scripts
1. formater - Tool for generating user names and email addresses.

### Help:
```
python formater.py -h
usage: formater.py [-h] [-n FILE] [-f FORMAT [FORMAT ...]] [-d DOMAIN] [-o FILE] [-l]

Tool for generating user names and email addresses.

optional arguments:
  -h, --help            show this help message and exit
  -n FILE, --names FILE
                        Input file format: <first><space><last>
  -f FORMAT [FORMAT ...], --format FORMAT [FORMAT ...]
                        Output formats: I.L F.L FL IL, FL@ F.L@ I.L@ IL@
  -d DOMAIN, --domain DOMAIN
                        Email Domain: example.com
  -o FILE, --outfile FILE
                        Output file name
  -l, --list-formats    Print available output formats
```
### Formats:
```
  python formater.py -l
  [-f <FORMATS>] - I.L F.L FL IL FL@ F.L@ I.L@ IL@
  I.L:  <first_initial>.<last_name>
  F.L:  <first_initial>.<last_name>
  FL:  <first_name><last_name>
  IL:  <first_initial><last_name>
  FL@: <first_name><last_name>@<domain>
  F.L@: <first_initial>.<last_name>@<domain>
  I.L@: <first_initial>.<last_name>@<domain>
  IL@: <first_initial><last_name>@<domain>
```
### Usage:
```
python formater.py -n tmp -f IL I.L FL F.L I.L@ IL@ FL@ F.L@ -d example.com
flast
f.last
firstlast
first.last
f.last@example.com
flast@example.com
firstlast@example.com
first.last@example.com
```
