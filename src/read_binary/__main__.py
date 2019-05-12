import click

from models.virtual_machine import VirtualMachine


@click.command()
@click.option('-s', '--source-file', required=True)
def main(source_file):
    vm = VirtualMachine(num_regs=8)
    vm.run(source_file)


if __name__ == '__main__':
    main()
