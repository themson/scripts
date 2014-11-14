Scripts
=======
Collection of useful scripts



### Scripts
1. formatter - Tool for rule-based user name and email address generation.

### Help:
```
$ python formatter.py -h                                     
usage: formatter.py [-h] [-n FILE] [-f RULESETS [RULESETS ...]] [-s RULESET]
                   [-d DOMAIN] [-o FILE] [-l]

Tool for rule-based user name and email address generation.

optional arguments:
  -h, --help            show this help message and exit
  -n FILE, --names FILE
                        Input file format: <first><space><last>
  -f RULESETS [RULESETS ...], --formats RULESETS [RULESETS ...]
                        Primary Formats: [F, f, L, l, ., -, _, s, d, ", ', <]
  -s RULESET, --secondary-format RULESET
                        Secondary Format: <primary format data> [F, f, L, l,
                        ., -, _, s, d, ", ', <]
  -d DOMAIN, --domain DOMAIN
                        Email Domain: example.com
  -o FILE, --outfile FILE
                        Output file name
  -l, --list-rules      Print formatting rules table
```
### Formatting Rules:
```
$ python formatter.py -l

------ Rules ------
F:  <fist_name>
f:  <last_initial>
L:  <last_name>
l:  <last_initial>
.:  delimiter <.>
-:  delimiter <->
_:  delimiter <_>
s:  delimiter <space>
d:  <domain_name>
":  wrapper "[username||email]"
':  wrapper '[username||email]'
<:  wrapper <[username||email]>
------------------

Example: formatter.py -n filename -f f.Ld -d example.com 
Output: f.last@example.com
```
### Usage Examples:
```
$ cat names.txt
First Last
Jane Doe

$ python formatter.py -n names.txt -f FL fL F.L f.L fLd F.Ld fLd lFd -d example.com
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

$ python formatter.py -n names.txt -f \"FsL -s \<f.Ld -d example.com
"first last" <f.last@example.com>
"jane doe" <j.doe@example.com>

```
