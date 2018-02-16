import decimal as dec


class _Symbolfr:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency


class _Symbolbr:
    def __init__(self, symbol, low_board, high_board):
        self.symbol = symbol
        self.low_board = low_board
        self.high_board = high_board


def _get_frequency(element):
    return element.frequency


def get_elements_board(dict_of_letters, symbol):
    for sym in dict_of_letters:
        if sym.symbol == symbol:
            return sym.low_board, sym.high_board


def get_symbols_frequency(user_string, precision=20):
    if precision <= 0:
        raise ValueError("Precision of encoding can not be less than zero")
    if len(user_string) == 0:
        raise ValueError("Received empty string")
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
            frequency_of_letters.append(_Symbolfr(ch_i, count))
        count = dec.Decimal(0)
    frequency_of_letters.sort(key=_get_frequency, reverse=True)
    return frequency_of_letters


def get_intervals_of_symbols(frequency_of_letters, precision=20):
    if precision <= 0:
        raise ValueError("Precision of encoding can not be less than zero")
    dec.getcontext().prec = precision
    vector_length = dec.Decimal(0)
    for sym in frequency_of_letters:
        if sym.frequency <= 0:
            raise ValueError("Frequency of symbol less than zero")
        vector_length += sym.frequency
    dict_of_letters = []
    length = dec.Decimal(0)
    for element in frequency_of_letters:
        low_board = length
        high_board = low_board + element.frequency / vector_length
        length += element.frequency / vector_length
        dict_of_letters.append(_Symbolbr(element.symbol, low_board, high_board))
    return dict_of_letters


def encode(user_string, precision=20):
    if precision <= 0:
        raise ValueError("Precision of encoding can not be less than zero")
    if len(user_string) == 0:
        raise ValueError("Received empty string")
    dec.getcontext().prec = precision
    vector_length = dec.Decimal(0)
    frequency_of_letters = get_symbols_frequency(user_string, precision)
    for sym in frequency_of_letters:
        if sym.frequency <= 0:
            raise ValueError("Frequency of symbol less than zero")
        vector_length += sym.frequency
    dict_of_letters = get_intervals_of_symbols(frequency_of_letters, precision)
    low_old = dec.Decimal(0)
    low_board = dec.Decimal(0)
    high_old = dec.Decimal(1)
    high_board = dec.Decimal(1)
    for ch in list(user_string):
        low, high = get_elements_board(dict_of_letters, ch)
        high_board = low_old + (high_old - low_old) * high
        low_board = low_old + (high_old - low_old) * low
        high_old = high_board
        low_old = low_board
    return low_board, high_board


def decode(frequency_of_letters, code, precision_of_string=10):
    if precision_of_string <= 0:
        raise ValueError("Precision of string can not be less than zero")
    if code < 0:
        raise ValueError("Code can not be less than zero")
    vector_length = dec.Decimal(0)
    for sym in frequency_of_letters:
        vector_length += sym.frequency
    dict_of_letters = get_intervals_of_symbols(frequency_of_letters, 38)
    first_char = ""
    for sym in frequency_of_letters:
        low, high = get_elements_board(dict_of_letters, sym.symbol)
        if low <= code <= high:
            first_char = sym.symbol
    user_string = [first_char]
    for i in range(0, precision_of_string - 1):
        low, high = get_elements_board(dict_of_letters, user_string[i])
        code = (code - low) / (high - low)
        for sym in frequency_of_letters:
            low, high = get_elements_board(dict_of_letters, sym.symbol)
            if low <= code <= high:
                user_string.append(sym.symbol)
    result_string = ""
    for ch in user_string:
        result_string += ch
    return result_string
