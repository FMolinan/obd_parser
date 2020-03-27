# OBD 2 Parser script

### This is a simple script for parsing the messages received from the OBD device. 

The purpose of these functions are to be embedded on a lambda function on AWS. In order to parse the messsages received on the IoT Core service and output the result to another channel in the SNS queue. The functions can also be used to read the raw logs in order to fetch specific information.

#### Installation:

Simply clone the repository or download the parser.py script directly

#### How to use:

Import the code and use accordingly

```Python
from parser import parse_message, parse_messages

raw_message =  "*TS01,861585040983700,201910130120,GPS:2;S33.440978;
W70.612985;0;0;3.02,STT:0;0,MGR:0,ADC:0;12.70;1;36.64;2;4.20,EVT:0#"

parse_message(raw_message)
>>> {'protocol': '01', 'device_id': '861585040983700', 
>>> 'timestamp': '201910130120', 'GPS': ['2', 'S33.440978', 'W70.612985', '0', '0', '3.02'], 
>>> 'STT': ['0', '0'], 'MGR': '0',
>>> 'ADC': ['0', '12.70', '1', '36.64', '2', '4.20'], 'EVT': '0'}

```

There are two main functions, *parse_message* expects a simple string, and *parse_messages* expect a list containing several strings (expected to be used in a service for example with a batch queue system).

#### Testing

Use the python builtin tester:

```batch 
$ python3 -m test
test_invalid_message (test_parser.ParserCase) ... ok
test_messages_with_errors (test_parser.ParserCase) ... ok
test_messsages (test_parser.ParserCase) ... ok
test_one_message (test_parser.ParserCase) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK

```

#### Contact info

reach us via mail to software@wisely.cl 
