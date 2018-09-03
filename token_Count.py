#! /usr/bin/env python3

import sys        # command line arguments
import re         # regular expression tools

#Reset the test file by writing to it nothing before
reset = open(sys.argv[2], 'w').close()
print("Welcome to Mystic Token Formatter!")

# set input and output files used this form wordCountTest.py
if len(sys.argv) is not 3:
    print("Correct usage: wordCountTest.py <input text file> <output file>")
    exit()

secargument = sys.argv[2]

#Dictionary
dictionary = {}

text_file = open(sys.argv[1], 'r')
#Lower case all the lines in said file
lines = text_file.read().lower()
#Uses regular expressions library re to find them all
reformatted = re.findall(r'\b[a-z]{1,15}\b', lines)

for word in reformatted:
    #grab the count of each word
    count = dictionary.get(word, 0)
    #added to our list if same instance of it
    dictionary[word] = count + 1

#grab keys and sort them in ascending order using sort function
token_list = dictionary.keys()
token_list = sorted(token_list)

#Read the token list that is sorted and write it to file
for words in token_list:
    f = open(secargument, "a")
    f.write(words)
    f.write(" ")
    f.write(str(dictionary[words]))
    f.write(("\n"))
f.close()
