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


if __name__ == '__main__':
    # convert(convertTr(input()))
    s = convertTr("/Users/shishi/PycharmProjects/wugniu/UTTRANSINFO_pure.txt")
    convert(s)
