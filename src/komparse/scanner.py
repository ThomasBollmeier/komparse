from collections import namedtuple
from .token_stream import TokenStream
from .char_stream import CharStream

Token = namedtuple('Token', 'types value')

class Scanner(object):
    
    def __init__(self, char_stream, grammar):
        self._char_stream = char_stream
        self._grammar = grammar
        self._remaining = []
        self._reader = StdReader(char_stream, self._grammar, self)
        
    def has_next(self):
        self._fill_buffer()
        return bool(self._remaining)
    
    def advance(self):
        self._fill_buffer()
        if self._remaining:
            return self._remaining.pop()
        else:
            return None
        
    def _fill_buffer(self):
        if not self._remaining:
            tokens = []
            while True:
                new_tokens = self._reader.next_tokens()
                if new_tokens is None:
                    break
                tokens += new_tokens
                if tokens:
                    break
            if tokens is not None:
                tokens.reverse()
                for token in tokens:
                    self._remaining.append(token)
        

class TokenReader(object):
    
    def __init__(self, char_stream, grammar, scanner):
        self._char_stream = char_stream
        self._grammar = grammar
        self._scanner = scanner
        self._chars = ""
        
    def next_tokens(self):
        raise NotImplementedError()
    
    def _init_chars(self, chars):
        self._chars = chars
    
    def _peek_next_char(self):
        if self._char_stream.has_next():
            return self._char_stream.peek()
        else:
            return None
        
    def _advance_char(self):
        self._chars += self._char_stream.advance()
        

class StdReader(TokenReader):
    
    def __init__(self, char_stream, grammar, scanner):
        TokenReader.__init__(self, char_stream, grammar, scanner)
        self._wspace = self._grammar.get_whitespace_chars()
        
    def next_tokens(self):
        while True:
            ch = self._peek_next_char()
            if ch is None:
                if self._chars:
                    tokens = self._create_tokens()
                    self._chars = ""
                    return tokens
                else:
                    return None
            if ch in self._wspace:
                tokens = self._create_tokens()
                self._scanner._reader = WSpaceReader(self._char_stream, self._grammar, self._scanner)
                return tokens
            self._advance_char()
            starts_comment, start, end = self._is_comment_start()
            if starts_comment:
                self._chars = self._chars[:len(self._chars)-len(start)]
                tokens = self._create_tokens()
                reader = CommentReader(self._char_stream, self._grammar, self._scanner)
                reader.set_delimiters(start, end)
                reader._init_chars(start)
                self._scanner._reader = reader
                return tokens
            starts_string, start, end, esc = self._is_string_start()
            if starts_string:
                self._chars = self._chars[:len(self._chars)-len(start)]
                tokens = self._create_tokens()
                reader = StringReader(self._char_stream, self._grammar, self._scanner)
                reader.set_delimiters(start, end, esc)
                reader._init_chars(start)
                self._scanner._reader = reader
                return tokens
                    
    def _create_tokens(self):
        return self._chars and [Token(types=["TERM"], value=self._chars)] or []
            
    def _is_comment_start(self):
        comment_delims = self._grammar.get_comments()
        for start, end in comment_delims:
            tail = self._chars[-len(start):]
            if tail == start:
                return True, start, end
        return False, None, None

    def _is_string_start(self):
        string_delims = self._grammar.get_strings()
        for start, end, esc in string_delims:
            tail = self._chars[-len(start):]
            if tail == start:
                return True, start, end, esc
        return False, None, None, None


class WSpaceReader(TokenReader):
    
    def __init__(self, char_stream, grammar, scanner):
        TokenReader.__init__(self, char_stream, grammar, scanner)
        self._wspace = self._grammar.get_whitespace_chars()
        
    def next_tokens(self):
        while True:
            ch = self._peek_next_char()
            if ch is None or ch not in self._wspace:
                self._scanner._reader = StdReader(self._char_stream, self._grammar, self._scanner)
                return []
            self._advance_char()


class CommentReader(TokenReader):

    def __init__(self, char_stream, grammar, scanner):
        TokenReader.__init__(self, char_stream, grammar, scanner)
        self._start = ""
        self._end = ""
        
    def set_delimiters(self, start, end):
        self._start = start
        self._end = end
        
    def next_tokens(self):
        len_end = len(self._end)
        while True:
            if self._peek_next_char() is None:
                self._scanner._reader = StdReader(self._char_stream, self._grammar, self._scanner)
                return [Token(types=["COMMENT"], value=self._chars)]
                #return []
            self._advance_char()
            if self._chars[-len_end:] == self._end:
                self._scanner._reader = StdReader(self._char_stream, self._grammar, self._scanner)
                return [Token(types=["COMMENT"], value=self._chars)]
                #return []
            

class StringReader(TokenReader):

    def __init__(self, char_stream, grammar, scanner):
        TokenReader.__init__(self, char_stream, grammar, scanner)
        self._start = ""
        self._end = ""
        self._esc = ""
        
    def set_delimiters(self, start, end, esc):
        self._start = start
        self._end = end
        self._esc = esc
        
    def next_tokens(self):
        len_end = len(self._end)
        while True:
            if self._peek_next_char() is None:
                return None
            self._advance_char()
            if self._chars[-len_end:] == self._end:
                self._scanner._reader = StdReader(self._char_stream, self._grammar, self._scanner)
                return [Token(types=["STRING"], value=self._chars)]


        
        
                    
                