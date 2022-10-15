from enum import unique, IntEnum, auto

import opencc
import re
import os

__wrong_char_replacement = [(re.compile('%s' % x[0]), x[1]) for x in [
    ('呵', '嗬'),
    ('得噶', '搭界'),
    ('那噶', '能介'),
    ('噶子', '茄子'),
    ('噶头', '家头'),
    ('噶三胡', '解山河'),
    ('噶', '介'),
    ('呃', '亇'),
    ('撒拧', '啥人'),
    ('拧', '人'),
    ('组撒', '做啥'),
    ('做撒', '做啥'),
    ('吾', '我'),
    ('伐是', '弗是'),
    ('伐会的', '弗会得'),
    ('伐会', '弗会'),
    ('伐曾', '弗曾'),
    ('伐？', '𠲎？'),
    ('伐！', '𠲎！'),
    ('伐。', '𠲎。'),
    ('伐\n', '𠲎\n'),
    ('伐', '弗'),
    ('困高', '睏覺'),
    ('哴', '丄'),
    ('呀到', '夜到')
]]


def convertTr(string):
    converter = opencc.OpenCC('s2t')
    file = open(string, 'r')
    output = string + "_tr.txt"
    f = open(output, "w")
    for l in file.readlines():
        l = cleanWrongCharacters(l)
        f.write(converter.convert(l))
    file.close()
    f.close()
    return output


def cleanWrongCharacters(text):
    for regex, replacement in __wrong_char_replacement:
        text = re.sub(regex, replacement, text)
    return text


def convert(string):
    f = open(string, "r")
    output = string + "_pi.txt"
    f1 = open(output, "w")
    converter = opencc.OpenCC("/Users/shishi/PycharmProjects/wugniu/wc2ph.json")
    for l in f.readlines():
        f1.write(converter.convert(l))
    f.close()
    f1.close()


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


if __name__ == '__main__':
    # convert(convertTr(input()))
    s = convertTr("/Users/shishi/PycharmProjects/wugniu/UTTRANSINFO_pure.txt")
    convert(s)
