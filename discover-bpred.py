
#!/usr/bin/env python

# Marc Beitchman

import branchpredictor
import math

BHR_SIZE = None

# Constants that bound the parameter space.
MAX_BHR_SIZE = 12
MAX_SC_BITS = 4
MAX_PC_BITS = 10

def find_branch_history_register_size(bpred):
    global BHR_SIZE 
    # set the initial bht entry to true
    bpred.actual(0, True)
    i = 0
    # count the intermediate states until we get to the bht entry that was set to true
    # this works since each saturating counter in the BHT is set to a value 
    # such that it currently reads not taken, but with 1 increment will read "taken"
    while bpred.predict(0) == False:
        i += 1
        bpred.actual(0, False)

    BHR_SIZE = i
    return BHR_SIZE

def find_saturating_counter_bits(bpred):
    
    # test for saturating counter of size 1 bit
    ## make sure the counter is set to minium state
    for i in range(2):
        bpred.actual(0, False)
    
    ## flip the counter's state
    bpred.actual(0, True)
    
    ## loop through bhr's the original table entry can be set
    for i in range(BHR_SIZE):
        bpred.actual(0, False)

    ## test the state to see if it changed as expected
    if bpred.predict(0) == True:
        return 1

    ## reset the predictor
    bpred.reset()

    # test for saturating counter of size 2 bits
    ## make sure the counter is set to minium state
    for i in range(3):
        bpred.actual(0, False)

    ## update the counter's state
    bpred.actual(0, True)

    for i in range(BHR_SIZE):
        bpred.actual(0, False)
    ## update the counter's state again
    bpred.actual(0, True)

    ## test the state to see if it changed as expected
    for i in range(BHR_SIZE):
        bpred.actual(0, False)

    if bpred.predict(0) == True:
        return 2

    ## reset the predictor
    bpred.reset()
    
    # test for saturating counter of size 3 bits
    ## make sure the counter is set to minium state
    for i in range(6):
        bpred.actual(0, False)

    ## update the counter's state
    for i in range(4):
        for i in range(BHR_SIZE):
            bpred.actual(0, False)
        bpred.actual(0, True)

    ## test the state to see if it changed as expected
    for i in range(BHR_SIZE):
        bpred.actual(0, False)

    if bpred.predict(0) == True:
        return 3

    bpred.reset()

    # test for saturating counter of size 4 bits
    ## make sure the counter is set to minium state
    for i in range(9):
        bpred.actual(0, False)

    ## update the counter's state
    for i in range(8):
        for i in range(BHR_SIZE):
            bpred.actual(0, False)
        bpred.actual(0, True)

    ## test the state to see if it changed as expected
    for i in range(BHR_SIZE):
        bpred.actual(0, False)

    if bpred.predict(0) == True:
        return 4

    return None

def find_pc_bits_used(bpred):
    
    # the idea is to max out the number of
    # bht entries for each pc bit and then
    # see if the next value beyond the current range of
    # bits causes us to alias by giving us an unepected
    # value

    for i in range(1, MAX_PC_BITS+2):
        for k in range(2**i):
            for j in range(BHR_SIZE):
                bpred.actual(k, True)
        if bpred.predict(k+1) == True:
            return i-1

        bpred.reset()

    return 0

def find_branch_history_table_entries(bpred):
 
    #  calculate bht entries

    return 2 ** ( find_pc_bits_used(bpred) + BHR_SIZE)

def discover(bpred):
    # This function collects your results and returns them in a
    # dictionary. You can add/remove reset() calls or reorder the
    # calls to your functions if you wish, but please keep the
    # structure of the returned dictionary the same for our grading
    # scripts.
    results = {}
    bpred.reset()
    results['bhr size'] = find_branch_history_register_size(bpred)
    bpred.reset()
    results['saturating counter bits'] = find_saturating_counter_bits(bpred)
    bpred.reset()
    results['bht entries'] = find_branch_history_table_entries(bpred)
    return results

if __name__ == '__main__':
    # When run as a script, we'll analyze each of the provided branch
    # predictors.
    for name, bpred in branchpredictor.mystery_predictors:
        results = discover(bpred)
        print '%s:' % name
        for k, v in results.items():
            print '  %s: %s' % (k, v)
        print