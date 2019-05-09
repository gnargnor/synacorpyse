import struct


def by2(f):
    rec = 'x'  # placeholder for the `while`
    while rec:
        rec = f.read(2)
        if rec:
            pos = struct.unpack('<H', rec)
            if pos[0] == 19:
                next = f.read(2)
                ascii_num = struct.unpack('<H', next)[0]
                yield chr(ascii_num)


def read_binary(file):
    with open(file, 'rb') as inh:
        output_characters = []
        [output_characters.append(char) for char in by2(inh) if char]
        out_string = ''.join(output_characters)
        return out_string
