import decimal as dec


class _Symbol:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency


class _Board:
    def __init__(self, low_board, high_board):
        self.low_board = low_board
        self.high_board = high_board


def _get_frequency(element):
    return element.frequency


def get_symbols_frequency(user_string, precision=20):
    dec.getcontext().prec = precision
    array_of_letters = []
    for ch in list(user_string):
            array_of_letters.append(ch)
    array_of_letters.sort()
    frequency_of_letters = []
    count = dec.Decimal(0)
    for ch_i in list(array_of_letters):
        for ch_g in list(array_of_letters):
            if ch_i == ch_g:
                count += dec.Decimal(1)
        is_exist = False
        for sym in frequency_of_letters:
            if sym.symbol == ch_i:
                is_exist = True
        if not is_exist:
            frequency_of_letters.append(_Symbol(ch_i, count))
        count = dec.Decimal(0)
    frequency_of_letters.sort(key=_get_frequency, reverse=True)
    return frequency_of_letters


def get_intervals_of_symbols(frequency_of_letters, precision=20):
    dec.getcontext().prec = precision
    vector_length = dec.Decimal(0)
    for sym in frequency_of_letters:
        vector_length += sym.frequency
    dict_of_letters = dict()
    length = dec.Decimal(0)
    for element in frequency_of_letters:
        dict_of_letters[element.symbol] = _Board(length, 0)
        length += element.frequency / vector_length
        dict_of_letters[element.symbol] = _Board(dict_of_letters[element.symbol].low_board, length)
    return dict_of_letters


def encode(frequency_of_letters, user_string, precision=20):
    dec.getcontext().prec = precision
    vector_length = dec.Decimal(0)
    for sym in frequency_of_letters:
        vector_length += sym.frequency
    dict_of_letters = get_intervals_of_symbols(frequency_of_letters, precision=38)
    low_old = dec.Decimal(0)
    low_board = dec.Decimal(0)
    high_old = dec.Decimal(1)
    high_board = dec.Decimal(1)
    for ch in list(user_string):
        high_board = low_old + (high_old - low_old) * dict_of_letters[ch].high_board
        low_board = low_old + (high_old - low_old) * dict_of_letters[ch].low_board
        high_old = high_board
        low_old = low_board
    return low_board, high_board


def decode(frequency_of_letters, code, precision_of_string=10):
    vector_length = dec.Decimal(0)
    for sym in frequency_of_letters:
        vector_length += sym.frequency
    dict_of_letters = dict()
    length = dec.Decimal(0)
    for element in frequency_of_letters:
        dict_of_letters[element.symbol] = _Board(length, 0)
        length += element.frequency / vector_length
        dict_of_letters[element.symbol] = _Board(dict_of_letters[element.symbol].low_board, dec.Decimal(length))
    first_char = ""
    for sym in frequency_of_letters:
        if dict_of_letters[sym.symbol].low_board <= code <= dict_of_letters[sym.symbol].high_board:
            first_char = sym.symbol
    user_string = [first_char]
    for i in range(0, precision_of_string - 1):
        code = (code - dict_of_letters[user_string[i]].low_board) / \
                    (dict_of_letters[user_string[i]].high_board - dict_of_letters[user_string[i]].low_board)
        for sym in frequency_of_letters:
            if dict_of_letters[sym.symbol].low_board <= code <= dict_of_letters[sym.symbol].high_board:
                user_string.append(sym.symbol)
    result_string = ""
    for ch in user_string:
        result_string += ch
    return result_string

