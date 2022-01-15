import click


@click.command()
@click.argument("file", type=click.File("r"))
def cli(file):
    main(file)
    click.echo("Hello World!")


import ast

def main(file):
    tree = ast.parse(file.read())
    return tree

if __name__ == "__main__":
    exit(cli())
