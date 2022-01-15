import click
import ast
import typing as t


def import_from_url(url: str):
    import requests as __r
    content = __r.get(url).text
    try:
        globs = {
            k: i for k, i in globals().items() if k.startswith("__")
        } | {"__import_from_url": import_from_url}
        exec(compile(main(url, content)[0], url, "exec"), globs)
    except Exception as e:
        print("***| Failed to load module from url:", url, "\n   |", e)
        return None
    return type(url, (), globs)


@click.command()
@click.argument("file", type=click.File("r"))
def cli(file):
    run(*main(str(file), file.read()))


def main(name, content):
    tree = ast.parse(content)
    tree = Importer().visit(tree)
    ast.fix_missing_locations(tree)
    return tree, name


def run(tree, name):
    code = compile(tree, str(name), "exec")
    exec(
        code,
        {
            "__file__": str(name),
            "__name__": "__main__",
            "__import_from_url": import_from_url,
        }
    )


if __name__ == "__main__":
    exit(cli())
