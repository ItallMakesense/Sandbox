# 13.06.17 ####################################################################
# def custom_sort(strings):
#     """ Takes a list of strings containing integers and words
#         and returns a sorted version of the list. The output
#         maintain the positions of strings and numbers as they
#         appeared in the original string """
#     words = iter(sorted(word for word in strings if word.isalpha()))
#     numbers = iter(sorted(num for num in strings if not num.isalpha()))
#     return " ".join(next(words) if string.isalpha() else next(numbers)\
#             for string in strings)

# strings = input("Enter objects row: ").split()
# print(custom_sort(strings))
# 23.06.17 ####################################################################
# """
# Need to finish encode function
# """
# import math
# class Morse:
#     @classmethod
#     def encode(cls, message):
#         bitwise = int(32)
#         morse = ''.join(cls.alpha[c] + '000' if c != ' ' else '0000'\
#                         for c in message)
#         morse = morse.ljust(bitwise * math.ceil(len(morse) / bitwise), '0')\
#                 if len(morse) % bitwise else morse
#         packed = [int(morse[i:i+bitwise], 2) for i in range(0, len(morse), bitwise)]
#         return [n - (1 << bitwise) for n in packed]

#     @classmethod
#     def decode(cls, array):
#         morse = ''.join(bin(i & 0xffffffff).lstrip('0b') for i in array)
#         letters = []
#         for w in morse.rstrip('0').split('0000000'):
#             for l in w.split('000'):
#                 letters.append(l)
#             letters.append('0')
#         letters.pop()
#         msg = []
#         for l in letters:
#             for k, v in cls.alpha.items():
#                 if v == l:
#                     msg.append(k)
#                     break
#         return ''.join(msg)

#     alpha = {
#         'A': '10111',
#         'B': '111010101',
#         'C': '11101011101',
#         'D': '1110101',
#         'E': '1',
#         'F': '101011101',
#         'G': '111011101',
#         'H': '1010101',
#         'I': '101',
#         'J': '1011101110111',
#         'K': '111010111',
#         'L': '101110101',
#         'M': '1110111',
#         'N': '11101',
#         'O': '11101110111',
#         'P': '10111011101',
#         'Q': '1110111010111',
#         'R': '1011101',
#         'S': '10101',
#         'T': '111',
#         'U': '1010111',
#         'V': '101010111',
#         'W': '101110111',
#         'X': '11101010111',
#         'Y': '1110101110111',
#         'Z': '11101110101',
#         '0': '1110111011101110111',
#         '1': '10111011101110111',
#         '2': '101011101110111',
#         '3': '1010101110111',
#         '4': '10101010111',
#         '5': '101010101',
#         '6': '11101010101',
#         '7': '1110111010101',
#         '8': '111011101110101',
#         '9': '11101110111011101',
#         '.': '10111010111010111',
#         ',': '1110111010101110111',
#         '?': '101011101110101',
#         "'": '1011101110111011101',
#         '!': '1110101110101110111',
#         '/': '1110101011101',
#         '(': '111010111011101',
#         ')': '1110101110111010111',
#         '&': '10111010101',
#         ':': '11101110111010101',
#         ';': '11101011101011101',
#         '=': '1110101010111',
#         '+': '1011101011101',
#         '-': '111010101010111',
#         '_': '10101110111010111',
#         '"': '101110101011101',
#         '$': '10101011101010111',
#         '@': '10111011101011101',
#         ' ': '0'
#         }

# print(Morse.encode('HELLO WORLD'))
# print(Morse.decode([-1440552402, -1547992901, -1896993141, -1461059584]))
# 24.06.17 ####################################################################
# def same_structure_as(one, two):
#     if not all(map(lambda _: type(_) in [list, set, dict], [one, two])):
#         return not any(map(lambda _: type(_) in [list, set, dict], [one, two]))
#     for i, v in enumerate(one):
#         same = same_structure_as(v, two[i]) if i < len(two) else False
#         if not same:
#             return False
#     return isinstance(one, type(two))

# print(same_structure_as([ 1, 1, 1 ], [ 2, 2, 2 ]))
# print(same_structure_as([ 1, [ 1, 1 ] ], [ 2, [ 2, 2 ]]))

# print(same_structure_as([ 1, [ 1, 1 ] ], [ [ 2, 2 ], 2 ]))
# print(same_structure_as([ 1, [ 1, 1 ] ], [ [ 2 ], 2 ]))

# print(same_structure_as([ [ [ ], [ ] ] ], [ [ [ ], [ ] ] ] ))
# print(same_structure_as([ [ [ ], [ ] ] ], [ [ 1, 1 ] ]))

# print(same_structure_as([1, '[', ']'], ['[', ']', 1]))
# 25.06.17 ####################################################################
# def justify(text, width):
#     """ Text justification in monospace font. Giving a single-lined text
#         and the expected justification width, it cuts the text on the strings
#         with given width. The longest word must not be greater than width.

#         Here are the rules:

#         - Use spaces to fill in the gaps between words.
#         - Each line should contain as many words as possible.
#         - Use '\n' to separate lines.
#         - Gap between words can't differ by more than one space.
#         - Lines should end with a word not a space.
#         - '\n' is not included in the length of a line.
#         - Large gaps go first, then smaller ones:
#             'Lorem---ipsum---dolor--sit--amet' (3, 3, 2, 2 spaces).
#         - Last line should not be justified, use only one space between words.
#         - Last line should not contain '\n'
#         - Strings with one word do not need gaps ('somelongword\n') """

#     words = text.split()
#     new = []
#     point = 0
#     while point <= len(words) - 1:
#         length = 0
#         sliced = words[point:point+width]
#         for i, word in enumerate(sliced):
#             between = 1 if i > 0 else 0
#             length += len(word) + between
#             if length > width:
#                 new.append(' '.join(sliced[:i]))
#                 point += i
#                 break
#             elif i == len(sliced) - 1:
#                 new.append(' '.join(sliced))
#                 point += i + 1
#                 break
#     for i, line in enumerate(new):
#         space = ' '
#         if line == new[-1]:
#             break
#         line = list(line)
#         item = 0
#         while len(line) < width and space in line:
#             if line[item] != space:
#                 single = True
#             elif single:
#                 line.insert(item, space)
#                 single = False
#             item += 1
#             item = item if item < len(line) else 0
#         new[i] = ''.join(line)
#     return '\n'.join(new)
# 00.00.00 ####################################################################
