from enum import Enum
import json
import sys

def basesugarunits(input_sequence):
    """
        Reads the input sequence (string) and returns the number of each of the different parts of the sequence
                Assumptions:
                1. The input_sequence is one string of length 4N-1 (where N is the number of bases)
                2. The input_sequence is not empty.
                Parameters:
                        input_sequence (string): input string containing base-sugar units and linkages
                Returns:
                        sequenceparts (dictionary): count of occurences of each of the different parts of the sequence

    """
    sequenceparts = {}
    for i in range(0, len(input_sequence), 4):
        if input_sequence[i:i+3] in sequenceparts:
            sequenceparts[input_sequence[i:i+3]] += 1
        else:
            sequenceparts[input_sequence[i:i+3]] = 1
        if i + 3 <= len(input_sequence)-1 and input_sequence[i+3] in sequenceparts:
                sequenceparts[input_sequence[i+3]] += 1
        elif i + 3<=len(input_sequence) - 1 and input_sequence[i+3] not in sequenceparts:
                sequenceparts[input_sequence[i+3]] = 1
    return sequenceparts

def calculate_mass(input_sequence, lookup_table):
    """
        Reads the input sequence (string) and lookup_table (dictionary) and returns the total mass of the sequence
                Assumptions:
                1. The input_sequence is one string of length 4N-1 (where N is the number of bases)
                2. The input_sequence is not empty.
                3. The lookup_table is a dictionary where the key is sequence part and value is the mass of the part
                   as a float (i.e. {'-Ur': 1.0001}.
                Parameters:
                        input_sequence (string): input string containing base-sugar units and linkages
                        lookup_table (dictionary): input dictionary containing molecular mass of each part
                Returns:
                        mass (float): total mass of the different parts of the sequence

    """
    output = basesugarunits(input_sequence)
    mass = 0
    #checking if the element in our input sequence is in lookup table, and if it is, add to the mass
    for element in output:
        if element in lookup_table:
            mass += output[element]*lookup_table[element] #incrementing the mass
        else:
            raise RuntimeError("Element {e} not found in lookup table".format(e=element) )
    return mass

def generateshippinglabel(input_sequence):
    """
        Reads the input sequence (string) and returns the number of each of the different parts of the sequence
                Assumptions:
                1. Any letter is allowed for the base (there is no error handling for the base)
                   and d is the only sugar that refers to DNA.
                2. The input_sequence is not empty
                3. The input_sequence is one string of length 4N-1 (where N is the number of bases)
                Parameters:
                        input_sequence (string): input string containing base-sugar units and linkages
                Returns:
                        shipping label (string): formatted shipping label of the input_sequence

    """
    bracket = False
    shippinglabel = ''
    for i in range(1,len(input_sequence),4):
        if input_sequence[i+1] == 'd' and not bracket:
            shippinglabel += '['+input_sequence[i]
            bracket = True
        elif input_sequence[i+1] != 'd' and bracket:
            shippinglabel += ']' + input_sequence[i]
            bracket = False
        else:
            shippinglabel += input_sequence[i]
    #This is closing the bracket if bracket was not closed (i.e. no RNA in the sequence at the end)
    if bracket:
        shippinglabel += ']'
    return shippinglabel

def sequencechecker(input_sequence):
    """
        Reads the input sequence (string) and returns the success or failure status, along with failure condition
        and position in sequence string where failure occured.
                Assumptions:
                1. The input_sequence is one string of length 4N-1 (where N is the number of bases)
                2. The input_sequence is not empty.
                Parameters:
                        input_sequence (string): input string containing base-sugar units and linkages
                Returns:
                        status (string): Success or Failure
                        failure_dict (dictionary): failure type and position in input_sequence where failured occured

        """
    modifiers = ['-', 'm', 'b', 'i']
    bases = ['A','G','C','T','U','I']
    sugars = ['d','r','m','f','a','i','p']
    linkages = ['o','s']
    failures_modifiers = []
    failures_bases = []
    failures_sugars = []
    failures_linkages = []
    status = 'Success'
    failure_dict = {}
    for i in range(0, len(input_sequence), 4):
        if input_sequence[i] not in modifiers:
            failures_modifiers.append(i)
            status = 'Failure'
        if input_sequence[i+1] not in bases:
            failures_bases.append(i+1)
            status = 'Failure'
        if input_sequence[i+2] not in sugars:
            failures_sugars.append(i+2)
            status = 'Failure'
        if i+3<len(input_sequence)-1 and input_sequence[i+3] not in linkages:
            failures_linkages.append(i)
            status = 'Failure'
    failure_dict['Unacceptable_modifiers'] = failures_modifiers
    failure_dict['Unacceptable_bases'] = failures_bases
    failure_dict['Unacceptable_sugars'] = failures_sugars
    failure_dict['Unacceptable_linkages'] = failures_linkages
    return status, failure_dict

class RunMode(Enum):
    RUN_BASE_SUGAR_UNITS = 1
    RUN_SEQUENCE_CHECKER = 2
    RUN_GENERATE_SHIPPING_LABEL = 3
    RUN_CALCULATE_MASS = 4

if __name__=='__main__':
    args = sys.argv[1:]

    if args[0] == RunMode.RUN_BASE_SUGAR_UNITS.name:
        if (len(args) != 2):
            print("Invalid number of arguments")
        else:
            print(basesugarunits(args[1]))
    elif args[0] == RunMode.RUN_SEQUENCE_CHECKER.name:
        if (len(args) != 2):
            print("Invalid number of arguments")
        else:
            print(sequencechecker(args[1]))
    elif args[0] == RunMode.RUN_GENERATE_SHIPPING_LABEL.name:
        if (len(args) != 2):
            print("Invalid number of arguments")
        else:
            print(generateshippinglabel(args[1]))
    elif args[0] == RunMode.RUN_CALCULATE_MASS.name:
        if (len(args) != 3):
            print("Invalid number of arguments")
        else:
            print(calculate_mass(args[1], json.loads(args[2])))
    else:
        print("Invalid function")

