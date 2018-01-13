import sys
sys.path.append("../src")
from komparse.token_stream import TokenStream

tokens = [1, 2, 3, 4, 5]

stream = TokenStream(tokens)

cnt = 0
stream.open_transaction()
while stream.has_next():
    print(stream.advance())
    cnt += 1
    if cnt == 2:
        stream.undo()