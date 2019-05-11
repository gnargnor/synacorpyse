import click

from models.source import SourceFile
from models.token import Tokens


@click.command()
@click.option('-s', '--source-file', required=True)
def main(source_file):
    source_file = SourceFile(source_file)
    input_values = source_file.interpret_binary()
    tokenizer = Tokens(input_values)
    tokens = [token for token in tokenizer]
    print(tokens)


if __name__ == '__main__':
    main()
