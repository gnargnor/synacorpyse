# Synacor Challenge
A Python VM implementation of the [Synacor Challenge](https://challenge.synacor.com/) architecture spec.

## About
Architecture specs and instructions in `challenge/arch-spec`

## Setup
* Create & activate virtual environment: `python3.7 -m venv venv && source venv/bin/activate && pip install --upgrade pip`
* Install local packages, dependencies, and console scripts declared in setup.py: `pip install -e .`

## What exactly is it that you do here?
**In Progress**
The challenge is to implement a VM to read the bytecode provided in the initial download.

Correctly processing the bytecode seems to require further steps indicated in the text produced.

* Run the VM: `read-binary -s challenge/challenge.bin`
* The VM will read the binary and tokenize the values interpreted from the binary.
* Working through the self tests: 21/21 operations implemented!

Printing characters written to memory indicates all operations work as intended and reveals text of
game based instructions.  However, after printing the output using the flag in the opcode, the output encoding changes
and subsequently changes the encoding of the shell session.

The output has been saved to the challenge directory as "output_after_initial_self-test_passes.txt"

The error message returned indicates a nonzero reg.  Next step is figuring out how to start the game that's been written
 to memory.

## Author
* Logan Kelly
