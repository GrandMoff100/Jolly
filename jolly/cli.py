import click
import ast
import typing as t


def import_from_url(url: str):
    import requests as __r
    content = __r.get(url).text
    try:
        globs = {k: i for k, i in globals().items() if k.startswith("__")}
        exec(content, globs)
    except Exception as e:
        print("***| Failed to load module from url:", url, "\n   |", e)
        return None
    return type(url, (), globs)


@click.command()
@click.argument("file", type=click.File("r"))
def cli(file):
    tree = main(file)
    code = compile(tree, str(file), "exec")
    exec(
        code,
        {
            "__file__": str(file),
            "__name__": "__main__",
            "__import_from_url": import_from_url,
        }
    )


class Importer(ast.NodeTransformer):
    @staticmethod
    def modify_expr(
        expr: ast.Expr
    ):
        if (
            isinstance(expr.value, ast.BinOp)
            and isinstance(expr.value.left, ast.UnaryOp)
            and isinstance(expr.value.left.op, ast.Invert)
            and isinstance(expr.value.op, ast.MatMult)
            and isinstance(expr.value.right, ast.Constant)
            and isinstance(expr.value.right.value, str)
        ):
            return ast.Assign(
                targets=[ast.Name(id=expr.value.left.operand.id, ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Name(id="__import_from_url", ctx=ast.Load()),
                    args=[ast.Constant(value=expr.value.right.value)],
                    keywords=[],
                )
            )

        return expr

    def visit_Expr(self, node: ast.Expr) -> t.Any:
        node = self.modify_expr(node)
        super().generic_visit(node)
        return node


def main(file):
    tree = ast.parse(file.read())
    tree = Importer().visit(tree)
    ast.fix_missing_locations(tree)
    return tree


if __name__ == "__main__":
    exit(cli())
