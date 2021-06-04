# Webber
Tool to Pentest
A tool developed for pentest, very beta!
It's recent!

Example:

> webber.py -u "https://www.google.com"

> webber.py -u "https://www.google.com/?param=1" --skip-params

> webber.py -u "https://www.google.com/?param=1" --skip-fuzzer

### or best examples:

`webber.py -u "https://www.google.com/?param=1" -sr -sf `


## Help commands

```optional arguments:
  -h, --help          show this help message and exit
  -u URL, --url URL   Indicar o URL
  -v, --version       Indicate the version of this tool
  -sr, --skip-rate    Skip the Rate limiting
  -sf, --skip-fuzzer  Skip the Fuzzer
  -sp, --skip-params  Skip the Params scanner
  --update            Update the tool```
