import click

from models.token import Tokens
from models.virtual_machine import VirtualMachine


@click.command()
@click.option('-s', '--source-file', required=True)
def main(source_file):
    vm = VirtualMachine(num_regs=8)
    # input_values = source_file.interpret_binary()
    # tokenizer = Tokens(input_values)
    # tokens = [token for token in tokenizer]
    # print(tokens)


if __name__ == '__main__':
    main()
