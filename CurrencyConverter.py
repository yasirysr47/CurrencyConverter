#!/usr/bin/python3
import os
import ast
import json
import argparse
from forex_python.converter import CurrencyRates
from CurrencyConverterUtils import CURRENCY_SYMBOL_MAP, DEFAULT_CURRENCY, init_logger, write_to_file, exchange_rate_file



class CurrencyConverter:
    def __init__(self):
        self.logger = init_logger()
        self.options = self.args_options()
        self.currency = CurrencyRates()
        self.exchange_rate = dict() #hash table to store the repeated exchange rates
        self.target_currency = self.options.target_currency.upper()
        if not len(self.currency.get_rates(DEFAULT_CURRENCY)):
            #CurrencyRates is not available
            self.load_previous_exchange_rate()

    def load_previous_exchange_rate(self):
        '''
        load previous exchange rate in case the 3rd party tools fail or broken
        '''
        fp = open(exchange_rate_file)
        self.exchange_rate = ast.literal_eval((ast.literal_eval(fp.read())))
        fp.close()

    def exchange_currency(self, currency_id, target_id=DEFAULT_CURRENCY, value=0):
        '''
        since this is not a live exchanging process
        I will store repeated exchange rates in a hash table.
        '''
        #edge cases to be handeld are: ensurre type of value is digits, currency sy,bols are correct
        if (currency_id, target_id) not in self.exchange_rate:
            rate = self.currency.get_rate(currency_id, target_id)
            self.exchange_rate[(currency_id, target_id)] = rate
        else:
            rate = self.exchange_rate.get((currency_id, target_id), 0)
        
        new_rate = rate * value
        return "{:.2f}".format(new_rate)

    def convert_currency_values(self):
        self.logger.info("Program Started")
        if self.options.server_mode:
            #starting server
            self.logger.info("Server Started")
            os.system('./server.py')
            return
        if not self.options.file or not os.path.exists(self.options.file):
            self.logger.error("Input file is not provided..... Terminating the program")
            return
        
        with open(self.options.file) as fp:
            list_converted_values = []
            # read each input line and cinvert the amount
            for line in fp:
                data = {}
                converted_data = {}
                try:
                    data = json.loads(line)
                except:
                    #handle invalid input records
                    self.logger.error("Invalid JSON record found in the input file.\nSkipping the record {}".format(line))
                    continue

                value = data.get("value", 0)
                currency = data.get("currency")
                if not value and not currency:
                    #empty record or incomplete records are handled here
                    self.logger.warning("Empty data record found in the input file.")
                    continue
                #get generalised currency symbol
                currency_id = CURRENCY_SYMBOL_MAP.get(currency.lower(), DEFAULT_CURRENCY)

                converted_value = self.exchange_currency(currency_id, self.target_currency, value)
                converted_data = {"value": converted_value, "currency": self.target_currency}
                #Aesthetics
                if self.options.detailed_visual:
                    output = "The amount of {} {} is {} {} as of today".format(value, currency, converted_value, self.target_currency)
                    print(output)
                    self.logger.info(output)
                elif self.options.visual == True:
                    print(converted_data)
                
                if self.options.out_file:
                    list_converted_values.append(converted_data)
            
        if list_converted_values:
            write_to_file(list_converted_values, self.options.out_file)
            self.logger.info("converted exchange rates are succesfully written into {}".format(self.options.out_file))
        self.save_exchange_rate()
        self.logger.info("Program ended successfully")

    def save_exchange_rate(self):
        write_to_file([str(self.exchange_rate)], exchange_rate_file)

    
    def args_options(self):
        # Initialize parser
        parser = argparse.ArgumentParser()
        
        # Adding optional argument
        parser.add_argument("-f", "--file", default="input_test.txt", help = "Input text file with JSON value and currency data per line")
        parser.add_argument("-o", "--out-file", default=False, help = "Output text file with JSON value and currency data per line")
        parser.add_argument("-t", "--target-currency", default=DEFAULT_CURRENCY, help = "Enter the Target currency symbol. (EUR, USD, JPY)")
        ### additional options for aesthetic purposes
        parser.add_argument("-v", "--visual", default=True, help = "prints the converted currency value for each lines of input")
        parser.add_argument("-d", "--detailed-visual", default=False, help = "print detailed info in structured sentence.")
        ### enabling server mode for url based run
        parser.add_argument("-s", "--server-mode", default=False, help = "server will be created and open http://localhost:8000/ in browser")
        # Read arguments from command line
        args = parser.parse_args()
        return args

    # def do_multi_process(self):
    #     <code here for multi process>


if __name__ == "__main__":
    currency_converter = CurrencyConverter()
    currency_converter.convert_currency_values()
    # we can have a multi process function too for async parallel outputs.
    # currency_converter.do_multi_process()
