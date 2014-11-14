Scripts
=======
Collection of useful scripts



### Scripts
1. formater - Tool for rule-based user name and email address generation.

### Help:
```
$ python formater.py -h
usage: formater.py [-h] [-n FILE] [-f RULESET [RULESET ...]] [-d DOMAIN]
                   [-o FILE] [-l]

Tool for generating user names and email addresses.

optional arguments:
  -h, --help            show this help message and exit
  -n FILE, --names FILE
                        Input file format: <first><space><last>
  -f RULESET [RULESET ...], --format RULESET [RULESET ...]
                        Format Rules: <F>, <f>, <L>, <l>, <.>, <->, <_>, <d>
  -d DOMAIN, --domain DOMAIN
                        Email Domain: example.com
  -o FILE, --outfile FILE
                        Output file name
  -l, --list-rules      Print formatting rules table
```
### Formatting Rules:
```
$ python formater.py -l

------ Rules ------
'F':  <fist_name>
'f':  <last_initial>
'L':  <last_name>
'l':  <last_initial>
'.':  delimiter <.>
'-':  delimiter <->
'_':  delimiter <_>
'd':  <domain_name>
------------------

Example: formater.py -n filename -f f.Ld -d example.com 
Output: f.last@example.com
```
### Usage Example:
```
$ cat names.txt
First Last
Jane Doe

$ python formater.py -n tmp.txt -f FL fL F.L f.L fLd F.Ld fLd lFd -d example.com
firstlast
flast
first.last
f.last
flast@example.com
first.last@example.com
flast@example.com
lfirst@example.com
janedoe
jdoe
jane.doe
j.doe
jdoe@example.com
jane.doe@example.com
jdoe@example.com
djane@example.com
```
