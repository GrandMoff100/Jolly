import ast
import typing as t


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
                    args=[ast.Constant(value=expr.value.right.value), ast.Constant(value=expr.value.left.operand.id)],
                    keywords=[],
                )
            )

        return expr

    def visit_Expr(self, node: ast.Expr) -> t.Any:
        node = self.modify_expr(node)
        super().generic_visit(node)
        return node
