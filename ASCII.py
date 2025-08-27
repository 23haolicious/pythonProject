def text_to_ascii(text):
    ascii_codes = []
    for char in text:
        ascii_code = ord(char)
        ascii_codes.append(ascii_code)
    return ascii_codes
# Example usage:
text = "273299_1810059"
ascii_codes = text_to_ascii(text)
print("ASCII Codes:", ascii_codes)

# def ascii_to_text(ascii_codes):
#     text = ""
#     for code in ascii_codes:
#         char = chr(code)
#         text += char
#     return text
#
# ascii_codes = [
#
# 50, 53, 56, 54, 54, 53
# ]
# text = ascii_to_text(ascii_codes)
# print("Text:", text)
