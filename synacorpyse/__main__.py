import click

from synacorpyse.virtual_machine import VirtualMachine


@click.command()
@click.option('-s', '--source-file', required=True)
def main(source_file):
    vm = VirtualMachine(num_regs=8)
    vm.load(source_file)
    vm.run()


if __name__ == '__main__':
    main()
