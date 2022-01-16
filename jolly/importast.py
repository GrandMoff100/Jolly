import ast


class Importer(ast.NodeTransformer):
    """Transforms the AST to use URL imports."""
    @staticmethod
    def modify_expr(
        expr: ast.AugAssign
    ):
        if (
            isinstance(expr, ast.AugAssign)
            and (isinstance(expr.target, ast.Attribute) or isinstance(expr.target, ast.Name))
            and isinstance(expr.op, ast.MatMult)
            and isinstance(expr.value, ast.Constant)
            and isinstance(expr.value.value, str)
        ):
            return ast.Assign(
                targets=[ast.Name(id=unwrap_attribute(expr.target), ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Name(id="import_url", ctx=ast.Load()),
                    args=[ast.Constant(value=expr.value.value), ast.Constant(value=unwrap_attribute(expr.target))],
                    keywords=[],
                )
            )

        return expr

    def visit_AugAssign(self, node: ast.AugAssign) -> ast.Assign:
        """Visits each AugAssign node and replaces it with a URL import if it is MatMul."""
        node = self.modify_expr(node)
        super().generic_visit(node)
        return node


def unwrap_attribute(node: ast.Attribute | ast.Name) -> str:
    """Unwraps an attribute node to get the name of the attribute."""
    if hasattr(node, "value") and isinstance(node.value, ast.Attribute):
        return unwrap_attribute(node.value) + "." + node.attr
    if hasattr(node, "value") and isinstance(node.value, ast.Name):
        return node.value.id + "." + node.attr
    return node.id
