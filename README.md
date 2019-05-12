# Synacor Challenge
A Python VM implementation of the [Synacor Challenge](https://challenge.synacor.com/) architecture spec.

## About
Architecture specs and instructions in `challenge/arch-spec`

## Setup
* Create & activate virtual environment: `python3.7 -m venv venv && source venv/bin/activate && pip install --upgrade pip`
* Install local packages, dependencies, and console scripts declared in setup.py: `pip install -e .`

## What exactly is it that you do here?
**In Progress** (Not much yet.)
* Run the VM: `read-binary -s challenge/challenge.bin`
* The VM will read the binary and tokenize the values interpreted from the binary.
* Working through the self tests: 16/21 operations implemented.

## Author
* Logan Kelly
