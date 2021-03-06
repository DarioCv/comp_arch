'''
Filename: pipeline_stages.py
Author:   Lucas Halbert
Date:     4/15/15
Modified: 4/16/15
Comment:  
'''
import sys
import re
import json

#NEEDS TO FLAG HAZARDS

'''
Class declarations for each stage of the pipeline
'''
class INSTRUCTIONFetch(object):
    '''
    This class is used to fetch an instructions from the instruction memory and place it 
    into the instruction register for decoding.
    '''

    def __init__(self, location):
        '''
        This constructor initializes
        '''

    def fetchFromMem(self):
        '''
        '''
        # Open instruction memory object and fetch the instruction pointed to by the stack pointer

        # Place the fetched instruction in the instruction register




class INSTRUCTIONDecode(object):
    '''
    This class is used to decode instructions passed to it. The instruction dictionary
    contains all specific bit mappings for each instruction operand. 
    '''

    def __init__(self, instruction):
        '''
        This constructor initilizes the instruction variable and splits it into its proper
        fields based on the last character of the op portion. If an "i" is present, the 
        instruction is expecting field[3] to be an immediate value.
        '''
        # Read and Open dictionary file relative to root of project
        self.inst_dict = json.loads(open("dictionaries/instruction_dictionary.py").read())
        # Initialize instuction
        self.instruction = instruction
        print("Instruction:",self.instruction)


    #def splitFields(self):
        '''
        This constructor splits the instruction string into usable fields.
        '''
        # Split instruction by "," and store in inst_fields
        self.inst_fields = self.instruction.split(',')
        print("Instruction Fields:",self.inst_fields)
        #return self.inst_fields


    def decodeOpField(self):
        '''
        This constructor decodes the OP field of the instruction.
        '''

        # Extract Instruction Operator from field 0
        self.inst_op = self.inst_fields[0]
        print("Instruction OP:",self.inst_op)

        # Check if 4th character of Operator specifies immediate value
        if self.inst_op[len(self.inst_op)-1] == "i":
            self.immediate = 1
        else:
            self.immediate = 0
        print("Immediate?:",self.immediate)

        self.inst_op_bin = self.inst_dict[self.inst_fields[0]]
        print("Instruction OP:",self.inst_fields[0])
        print("Instruction OP Binary:",self.inst_op_bin)


    def decodeDestField(self):
        '''
        This constructor decodes the destination field of the instruction
        '''

        # Extract instruction destination from field 1
        self.inst_dest = self.inst_fields[1]
        print("Instruction Destination:",self.inst_dest)

        # Error check to confirm that field 1 does not contain a register that does not exist(>31)
        if int(self.inst_dest.split('$')[1]) > 31:
            print("Register",self.inst_dest,"does not exist")
            sys.exit(4)

        # Convert instruction destination to binary and pad to 5 bits MSB
        self.inst_dest_bin = "{0:b}".format(int(self.inst_fields[1].split('$')[1])).rjust(5, '0')
        print("Instruction Dest Binary:",self.inst_dest_bin)


    def decodeSource1Field(self):
        '''
        This constructor decodes the source1 field of the instruction
        '''

        # Extract instruction source1 from field 2
        self.inst_source1 = self.inst_fields[2]
        print("Instruction Source1:",self.inst_source1)

        # Error check to confirm that field 2 does not contain a register that does not exist(>31)
        if int(self.inst_source1.split('$')[1]) > 31:
            print("Register",self.inst_source1,"does not exist")
            sys.exit(4)

        # Convert instruction source1 to binary and pad to 5 bits MSB
        self.inst_source1_bin = "{0:b}".format(int(self.inst_fields[2].split('$')[1])).rjust(5, '0')
        print("Instruction source1 Binary:",self.inst_source1_bin)


    def decodeSource2Field(self):
        '''
        This constructor decodes the source2 field of the instruction
        '''

        # Extract instruction source1 from field 3
        self.inst_source2 = self.inst_fields[3]
        print("Instruction Source2:",self.inst_source1)

        # Error check to confirm that field 3 does not contain a register that does not exist(>31)
        if int(self.inst_source2.split('$')[1]) > 31:
            print("Register",self.inst_source2,"does not exist")
            sys.exit(4)

        # Convert instruction source2 to binary and pad to 5 bits MSB
        self.inst_source2_bin = "{0:b}".format(int(self.inst_fields[3].split('$')[1])).rjust(5, '0')
        print("Instruction source2 Binary:",self.inst_source2_bin)


    def decodeImmediateValue(self):
        '''
        This constructor decodes the immediate value field of the instruction if self.immediate = 1
        '''

        # Extract instruction immediate value from field 3
        self.inst_immediate = self.inst_fields[3]
        print("Instruction Immediate:",self.inst_immediate)


        # Error check to confirm that field 3 does not contain a register that does not exist(>31)
        if int(self.inst_immediate.split('#')[1]) > 131071 :
            print("Values greater than 131071 cannot be entered")
            sys.exit(5)

        # Convert instruction immediate value to binary and pad to 17 bits LSB 
        self.inst_immediate_bin = "{0:b}".format(int(self.inst_fields[3].split('#')[1])).rjust(17, '0')
        print("Instruction Immediate Binary:",self.inst_immediate_bin)


    def constructByteCode(self):
        '''
        This constructor compiles all of the binary fields into a single 32 bit binary string to be passed
        to other stages of the pipeline.
        '''

        # Combine OP, Dest, Source1, and Source2 into compiled binary
        if self.immediate == 1:
            self.inst_bin = self.inst_op_bin + self.inst_dest_bin + self.inst_source1_bin + self.inst_immediate_bin
        elif self.immediate == 0:
            self.inst_bin = self.inst_op_bin + self.inst_dest_bin + self.inst_source1_bin + self.inst_source1_bin

        self.inst_bin_len = len(self.inst_bin)

        # Force 32 bit length
        self.inst_bin = self.inst_bin.ljust(32, '0')
        print("Instruction Length:",len(self.inst_bin))
        print("Complete Instruction Binary:",self.inst_bin)
