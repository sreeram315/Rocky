


def remove_char_from_string(string, char):
	returner = ''
	for ch in string:
		if ch != char:
			returner += ch
	return returner

def remove_chars_from_string(string, chars):
	returner = ''
	for ch in string:
		if ch not in chars:
			returner += ch
	return returner

