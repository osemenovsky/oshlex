import os
import shlex
import glob

class MandatoryOptionMissing(Exception):
    pass

class UnknownDirective(Exception):
    pass

class SyntaxError(Exception):
    pass

class ConfigError(Exception):
    pass


def stripmany(s, chars, w=False):
    for c in chars:
        s = s.strip(c)
    if w:
        s.strip()

    return s


class Rule():
    """
    Class, defining a rule, by which directive is handled
    """
    def __init__(self, name="root", handler=None, unique=False, mandatory=False):
        self.name = name
        self.handler = handler
        self.unique = unique
        self.mandatory = mandatory
        self.subrules = {}

    def __getitem__(self, key):
        return self.__dict__[key]

    def get(self, name):
        return self.subrules[name]

    def add(self, rule):
        self.subrules[rule.name] = rule

    def in_context(self, name):
        if name in self.subrules:
            return True

        else:
            return False

    def check(self, config):
        for k, v in self.subrules.items():
            if not k in config and v.mandatory:
                raise MandatoryOptionMissing("Missing mandatory option {}".format(k))


class Tokenizer(shlex.shlex):
    def __init__(self, instream=None, infile=None, posix=True):
        super(Tokenizer, self).__init__(instream=instream, infile=infile, posix=posix)
        self.wordchars += ',-./*@:'
        self.source = 'include'

    def sourcehook(self, newfile):
        "Hook called on a filename to be sourced."
        newfile = stripmany(newfile, ["\"", "\'"], w=True)
        # This implements cpp-like semantics for relative-path inclusion.
        if isinstance(self.infile, str) and not os.path.isabs(newfile):
            newfile = os.path.join(os.path.dirname(self.infile), newfile)
        filelist = glob.glob(newfile)
        for f in filelist:
            self.push_source(open(f, 'r'), f)


class Configuration():
    def __init__(self, root, path, tokenizer=None):
        self._path = path
        self._root = root
        if not tokenizer:
            self._tokenizer = Tokenizer
        else:
            self._tokenizer = tokenizer

        self.tokenizer = None
        self._config = {}

    def read(self):
        self.tokenizer = self._tokenizer(open(self._path, 'r'), infile=self._path)
        self._config = self._parse()

    def __str__(self):
        return str(self._config)

    def __repr__(self):
        return repr(self._config)

    def __getitem__(self, key):
        return self._config[key]

    def _parse(self, state=None):
        stack = []
        config = {}
        directive = None
        value = None
        if not state:
            state = self._root

        while True:
            token = self.tokenizer.get_token()
            if token == ";":
                if len(stack) >= 2:
                    rule = state.get(stack[0])
                    if rule.unique:
                        if stack[0] in config:
                            raise ConfigError("Unique directive already set: {}".format(stack[0]))
                        else:
                            try:
                                config[stack[0]] = rule.handler(stack[1:])
                            except Exception as e:
                                raise ConfigError("{}:{} Handler couldn't process tokens, got an exception {}".format(
                                    self.tokenizer.infile,
                                    self.tokenizer.lineno,
                                    e,
                                ))

                    else:
                        if not stack[0] in config:
                            config[stack[0]] = []

                        try:
                            config[stack[0]].append(rule.handler(stack[1:]))
                        except Exception as e:
                            raise ConfigError("{}:{} Handler couldn't process tokens, got an exception {} ".format(
                                self.tokenizer.infile,
                                self.tokenizer.lineno,
                                e,
                            ))

                    stack = []

                else:
                    raise ConfigError("Syntax error")

            elif token == "{":
                if len(stack) == 1:
                    rule = state.get(stack[0])
                    value = self._parse(rule)
                    if rule.unique:
                        if stack[0] in config:
                            raise ConfigError("Unique value already set")
                        else:
                            config[stack[0]] = value

                    else:
                        if not stack[0] in config:
                            config[stack[0]] = []
                        config[stack[0]].append(value)

                    stack = []

                else:
                    raise ConfigError("Syntax error")

            elif token == "}" or not token:
                if not stack:
                    state.check(config)

                    return config

                else:
                    raise ConfigError("Syntax error")

            else:
                if not stack:
                    if state.in_context(token):
                        stack.append(token)

                    else:
                        raise ConfigError("Unknown directive: {}".format(token))

                else:
                    stack.append(token)
