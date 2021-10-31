# CurrencyConverter

### Prerequisites installation Guide
* Python3 Installation Guide : https://www.python.org/downloads/
* forex_python library Installation Guide : https://forex-python.readthedocs.io/en/latest/installation.html

Other Libraries used:
```
os
ast
cgi
json
http
urllib
argparse
logging
```
These libraries are present by default in python3. If not do the following:
`pip3 install <library_name>`

## Introduction to the Scripts
The main script is called CurrencyConverter.py and it is the starting point for this service.
we have following arguments we can pass for vsarious options:
```
usage: ./CurrencyConverter.py [-h] [-f FILE] [-o OUT_FILE] [-t TARGET_CURRENCY] [-v VISUAL] [-d DETAILED_VISUAL] [-s SERVER_MODE]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Input text file with JSON value and currency data per line
  -o OUT_FILE, --out-file OUT_FILE
                        Output text file with JSON value and currency data per line
  -t TARGET_CURRENCY, --target-currency TARGET_CURRENCY
                        Enter the Target currency symbol. (EUR, USD, JPY)
  -v VISUAL, --visual VISUAL
                        prints the converted currency value for each lines of input
  -d DETAILED_VISUAL, --detailed-visual DETAILED_VISUAL
                        print detailed info in structured sentence.
  -s SERVER_MODE, --server-mode SERVER_MODE
                        server will be created and open http://localhost:8000/ in browser
```

##### Input file format
```
{ "value": 9.95, "currency": "USD" }
{ "value": 99.95, "currency": "JPY" }
{ "value": 10.99, "currency": "EUR" }
{ "value": 19.95, "currency": "USD" }
{ "value": 9249.95, "currency": "JPY" }
{ "value": 10.99, "currency": "EUR" }
{ "value": 94.95, "currency": "USD" }
{ "value": 10000, "currency": "JPY" }
{ "value": 140.99, "currency": "EUR"
```
##### Output file format
```
{'value': '9.95', 'currency': 'USD'}
{'value': '0.88', 'currency': 'USD'}
{'value': '12.80', 'currency': 'USD'}
{'value': '19.95', 'currency': 'USD'}
{'value': '81.22', 'currency': 'USD'}
{'value': '12.80', 'currency': 'USD'}
{'value': '94.95', 'currency': 'USD'}
{'value': '87.81', 'currency': 'USD'}
{'value': '164.18', 'currency': 'USD'}
```
##### Supporting Scripts:
* CurrencyConverterUtils.py : utility script that has some helper functions and configurable variables
* server.py : starts the server for the service

##### Supported Currencies:
```
USD
EUR
JPY
```


## Running the Program


1. Extract this folder to a directory
2. Move to this directory
3. Run any of the below mentiioned commands


-----------



#### Method 1: the default

**The Ouput is printed on the Terminal**

`./CurrencyConverter.py -f <input-file name> -t <target currency>`

Example 1:

`./CurrencyConverter.py -f small_input.txt -t usd`

this will take a input file "small_inputs.txt" and converts the values into the Target "USD".

the output is json line per record displayed on the terminal

Example 2:

`./CurrencyConverter.py -f large_input.txt -t jpy -d True`

this will take a input file "large_inputs.txt" and converts the values into the Target "JPY".

the output is displayed in a readable sentence.


-----------


#### Method 2: Save the Output
**The Ouput can be printed on the Terminal and Save it to a file**

`./CurrencyConverter.py -f <input-file name> -o <outfile_name> -t <target currency>`

Example 1:

`./CurrencyConverter.py -f small_input.txt -o small_output.txt -t usd -v False`

this will take a input file "small_inputs.txt" and converts the values into the Target "USD"

the output is not displayed on the terminal because of `-v Flase` flag

the output is written into `small_output.txt` file

Example 2:

`./CurrencyConverter.py -f large_input.txt -o large_output.txt -t jpy -d True`

this will take a input file "large_inputs.txt" and converts the values into the Target "JPY"

the output is displayed in a readable sentence.

the output is written into `large_output.txt` file


-----------


#### Method 3: Starting the Server
**The Ouput is displayed on the browser**

Run 
`./CurrencyConverter.py -s True`

Then Goto: http://localhost:8000/

there is a small GUI for interacting with the program.

other ways to evoke the API are:

`http://localhost:8000/convert?current_currency=<CURRENCY SYMBOL>&target_currency=<CURRENCY SYMBOL>&value=<AMOUNT>`

Example:

* To Start the Conversion directly : http://localhost:8000/convert?current_currency=usd&target_currency=eur&value=108723
* To Start the GUI directly : http://localhost:8000/convert
