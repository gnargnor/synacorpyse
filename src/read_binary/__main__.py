import click

import reader


@click.command()
@click.option('-f', '--file', required=True)
def main(file):
    out_string = reader.read_binary(file)
    print(out_string)


if __name__ == '__main__':
    main()
