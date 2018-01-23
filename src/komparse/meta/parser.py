from komparse.parser import Parser
from komparse.grammar import Grammar


def create_meta_parser():
    return Parser(MetaGrammar())


class MetaGrammar(Grammar):

    def __init__(self):
        Grammar.__init__(self)
        self._setup_tokens()
        self._setup_rules()

    def setup_tokens(self):
        pass

    def setup_rules(self):
        pass
