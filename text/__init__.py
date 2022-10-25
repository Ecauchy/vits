""" from https://github.com/keithito/tacotron """
from text import cleaners
from text.symbols import symbols, tone_symbols

# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}
_tone_symbol_to_id = {s: i for i, s in enumerate(tone_symbols)}
_tone_id_to_symbol = {i: s for i, s in enumerate(tone_symbols)}


def text_to_sequence(text, cleaner_names):
    '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
      Args:
        text: string to convert to a sequence
        cleaner_names: names of the cleaner functions to run the text through
      Returns:
        List of integers corresponding to the symbols in the text
    '''
    sequence = []
    tone_sequence = None

    clean_text, tones = _clean_text(text, cleaner_names)
    for symbol in clean_text:
        if symbol not in _symbol_to_id.keys():
            continue
        symbol_id = _symbol_to_id[symbol]
        sequence += [symbol_id]
    if tones:
        tone_sequence = tone_to_sequence(tones)
    return sequence, tone_sequence


def cleaned_text_to_sequence(cleaned_text):
    '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
      Args:
        text: string to convert to a sequence
      Returns:
        List of integers corresponding to the symbols in the text
    '''
    sequence = [_symbol_to_id[symbol] for symbol in cleaned_text if symbol in _symbol_to_id.keys()]
    return sequence


def tone_to_sequence(tone):
    '''Converts a string of tone to a sequence of IDs corresponding to the symbols in the tone.
      Args:
        tone: string to convert to a sequence
      Returns:
        List of integers corresponding to the symbols in the text
    '''
    sequence = [_tone_symbol_to_id[symbol] for symbol in tone if symbol in _tone_symbol_to_id.keys()]
    return sequence


def sequence_to_text(sequence):
    '''Converts a sequence of IDs back to a string'''
    result = ''
    for symbol_id in sequence:
        s = _id_to_symbol[symbol_id]
        result += s
    return result


def _clean_text(text, cleaner_names):
    tones = None
    for name in cleaner_names:
        cleaner = getattr(cleaners, name)
        if not cleaner:
            raise Exception('Unknown cleaner: %s' % name)
        text_with_tones = cleaner(text)
        try:
            text, tones = text_with_tones
        except ValueError:
            text = text_with_tones
    return text, tones
