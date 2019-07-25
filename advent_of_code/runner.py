import click


def adventrunner(func):
    """
    Advent of code runner decorator which decorate out a function for a simple CLI
    tool creation. Function which is decorated using a advent of code runner should
    return out a Initializer class so it can create out a CLI
    """

    def create_command():
        initializer_defined = func()

        @click.group()
        def main():
            """
            CLI tool created from a provided Initializer Object
            """
            pass

        @main.command(help="run a certain function defined inside a run function")
        @click.argument("name")
        def run(name):
            initializer_defined.run(name)

        @main.comman(help="run all function defined in a package")
        def all():
            initializer_defined.run_all()

        @main.command("list", help="list out all of the available function")
        def list_functions():
            initializer_defined.list_functions()

        return main()

    return create_command
