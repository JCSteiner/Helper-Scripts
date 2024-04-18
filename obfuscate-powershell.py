###############################################################################
# obfuscate-powershell.py
# one of many resources to obfuscate powrshell files
# this script will randomize all variable and function names

# load dependencies
import random
import string

# take our parameter inputs
infilePath = input('What is the filepath to your powershell file?')
outfilePath = input('What would you like to call your output file?')

# prints recommendation to the screen
if infilePath == outfilePath:
    print('Recommned you call them different filenames to avoid overwrite conflicts.')

# opens our two files
infile = open(infilePath, 'r')
outfile = open(outfilePath, 'w')

# this will store all varaible names and their replacements, so we can ensure we keep track
# of what has been replaced and what has not
vars = dict()

# gets random letters and numbers 
randletters = string.ascii_lowercase + string.ascii_uppercase + "0123456789"

# loops through every line in the powershell input script
for line in infile:

    # stores a copy of the file so we can edit it to replace special characters with spaces
    # we want to do this so that we can make sure "$x+" and "$x" are treated as the same variable (for example)
    line_copy = line
    line_copy = line_copy.replace('+', ' ')
    line_copy = line_copy.replace('-', ' ')
    line_copy = line_copy.replace(':', ' ')
    line_copy = line_copy.replace('+', ' ')
    line_copy = line_copy.replace('(', ' ')
    line_copy = line_copy.replace('[', ' ')
    line_copy = line_copy.replace(',', ' ')
    line_copy = line_copy.replace('.', ' ')
    line_copy = line_copy.replace(')', ' ')
    line_copy = line_copy.replace(']', ' ')

    # splits into every set of words so we can find the variables
    words = line_copy.split()

    # loops through each word
    for word in words:

        # if the first letter is a "$" and it is not a reserved or empty variable
        isvar = word[0] == "$" and word[1] != "_" and word.lower() != "$true" and word.lower() != "$false" and word.lower() != "$null"

        # if we found a variable and it is not already in our dictionary
        if isvar and word not in vars.keys():

            # generate a 16 character replacement and put in the dict
            vars[word] = '$' + ''.join(random.choice(randletters) for i in range(16))

        # if it is not a variable, but is a function
        elif word == "function":

            # generate a 16 character replacement and put it in the dictionary
            vars[words[words.index(word)+1]] = ''.join(random.choice(randletters) for i in range(16))

        # if the current word is in the dictionary (why we loop through each word)
        if word in vars.keys():
            # replace it with its replacement
            line = line.replace(word, vars[word])

    # writes the line to the output file
    outfile.write(line)

# prints the variables replaced
for var in vars:
    print('Variable', var, 'is replaced with',vars[var])


# closes file handles
infile.close()
outfile.close()

print('Final powershell file saved to:', outfilePath)
