from enum import unique, IntEnum, auto

import re
import os

def wide_used_tone_sandhi(characters):
    if len(characters) <= 2:
        return [manage_tone_symbols(x) for x in characters]

    # 1x式
    if characters[1] == '1':
        characters[1] = '˥˥'
        characters[-1] = '˨˩'
        for i in range(3, len(characters) - 2, 2):
            characters[i] = '˧˧'
    else:
        # 8x式
        if characters[1] == '8' and len(characters) <= 6:
            characters[1] = '˩˩'
            characters[-1] = '˨˧'
            if len(characters) == 6:
                characters[3] = '˨˨'
        else:
            # 6x式
            if characters[1] == '6':
                characters[1] = '˨˨'
            # 5x式 及 7x式
            else:
                characters[1] = '˧˧'

            if len(characters) == 4:
                characters[3] = '˦˦'
            else:
                characters[-1] = '˨˩'
                characters[3] = '˥˥'
                for i in range(5, len(characters) - 2, 2):
                    characters[i] = '˧˧'

    return characters


def narrow_used_tone_sandhi(words):
    flag = True
    result = []
    for word in words[:-1]:
        # word = manage_tone_marks(word, ToneStyle.MARK_WUDU)
        characters = [x for x in re.split(r'(\d+)', word) if x]
        characters = wide_used_tone_sandhi(characters)
        if flag and len(characters) == 2:
            if characters[-1] == '˨˧':
                characters[-1] = '˧˧'
            elif characters[-1] == '˩˨':
                characters[-1] = '˨˨'
            else:
                characters[-1] = '˦˦'
        else:
            characters[-1] = '˧˧'
        flag = len(characters) == 2
        result.append("".join(characters))
    word = words[-1]
    characters = [x for x in re.split(r'(\d+)', word) if x]
    characters = wide_used_tone_sandhi(characters)
    result.append("".join(characters))
    return result



def manage_tone_marks(text, from_tone_style):
    if from_tone_style == ToneStyle.NUM_WUDU:
        return text.replace('12', '8').replace('1', '8').replace('53', '1').replace('55', '7') \
            .replace('5', '7').replace('34', '5').replace('23', '6')
    elif from_tone_style == ToneStyle.MARK_WUDU:
        return text.replace('˩˨', '8').replace('˩', '8').replace('˥˧', '1').replace('˥˥', '7') \
            .replace('˥', '7').replace('˧˦', '5').replace('˨˧', '6')
    return text


def manage_tone_symbols(text):
    return text.replace('1', '˥˧').replace('5', '˧˦').replace('6', '˨˧').replace('7', '˥˥').replace('8', '˩˨')


@unique
class ToneStyle(IntEnum):
    NUM_WUDU = auto()
    MARK_WUDU = auto()
    SISHENG = auto()