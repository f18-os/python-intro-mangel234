#! /usr/bin/env python3

import sys        # command line arguments
import re         # regular expression tools

print("Welcome to Mystic Token Formatter!")

# set input and output files
if len(sys.argv) is not 3:
    print("Correct usage: wordCountTest.py <input text file> <output file>")
    exit()

secargument = sys.argv[2]


list = {}

text_file = open(sys.argv[1], 'r')
lines = text_file.read().lower()
#Uses regular expressions library re to find them all
reformatted = re.findall(r'\b[a-z]{3,15}\b', lines)

for word in reformatted:
    #grab the count of each word
    count = list.get(word, 0)
    #added to our list if same instance of it
    list[word] = count + 1
#grab keys and sort them in ascending order using sort function
token_list = list.keys()
token_list = sorted(token_list)

#Read the token list that is sorted and write it to file
f = open(secargument, "a")
for words in token_list:
    f.write(words)
    f.write(" ")
    f.write(str(list[words]))
    f.write(("\n"))
f.close()
