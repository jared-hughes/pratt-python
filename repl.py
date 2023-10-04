import cmd, traceback

from parse import parse, frame


class Shell(cmd.Cmd):
    intro = (
        "Basic syntax: 2*sin(pi)+1-(3/4)*5^6. Type :functions for a list of functions."
    )
    prompt = ">>> "
    file = None

    def precmd(self, line):
        if line in "" or line[0] == "?":
            return line
        elif line[0] == ":":
            return line[1:]
        else:
            return "eval " + line

    def do_eval(self, arg):
        "Evaluate an expression"
        try:
            val = parse(arg)
            print(val)
        except:
            traceback.print_exc(limit=0)

    def do_functions(self, _arg):
        "Print list of available functions."
        self.columnize(list(frame.keys()))


Shell().cmdloop()
