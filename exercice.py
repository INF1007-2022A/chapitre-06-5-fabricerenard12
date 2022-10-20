#!/usr/bin/env python
# -*- coding: utf-8 -*-


from numpy import full


def check_brackets(text, brackets):
	opening_brackets = dict(zip(brackets[0::2], brackets[1::2])) # Ouvrants à fermants
	closing_brackets = dict(zip(brackets[1::2], brackets[0::2])) # Fermants à ouvrants
	
	stack = []

	for i in text:
		if i in opening_brackets:
			stack.append(i)
		elif i in closing_brackets:
			if len(stack) == 0 or stack[-1] != closing_brackets[i]:
				return False

			stack.pop()

		return True if len(stack) == 0 else False
	

def remove_comments(full_text, comment_start, comment_end):

	if comment_start not in full_text and comment_end not in full_text:
		return full_text
	
	if comment_start in full_text:
		text_left = full_text.split(comment_start)
		text_left.pop()
		text_left = str(text_left[0])

		if comment_end in full_text:
			text_right = full_text.split(comment_end).pop()
			return text_left + text_right

	return None

	


def get_tag_prefix(text, opening_tags, closing_tags):
	res = ''

	for i in text:
		if res in opening_tags:
			return (res, None)
		elif res in closing_tags:
			return (None, res)
		res += i

	if res in opening_tags:
		return (res, None)
	elif res in closing_tags:
		return (None, res)
	else:
		return (None, None)


def check_tags(full_text, tag_names, comment_tags):
	text = remove_comments(full_text, *comment_tags)
	if text is None:
		return False

	# On construit nos balises à la HTML ("head" donne "<head>" et "</head>")
	opening_tags = {f"<{name}>": f"</{name}>" for name in tag_names} # Ouvrant à fermant
	closing_tags = dict((v, k) for k, v in opening_tags.items()) # Fermant à ouvrant

	# Même algo qu'au numéro 1, mais adapté aux balises de plusieurs caractères
	tag_stack = []
	while len(text) != 0:
		opening, closing = get_tag_prefix(text, opening_tags.keys(), closing_tags.keys())
		# Si ouvrant:
		if opening is not None:
			# On empile et on avance
			tag_stack.append(opening)
			text = text[len(opening):]
		# Si fermant:
		elif closing is not None:
			# Si pile vide OU match pas le haut de la pile:
			if len(tag_stack) == 0 or tag_stack[-1] != closing_tags[closing]:
				# Pas bon
				return False
			# On dépile et on avance
			tag_stack.pop()
			text = text[len(closing):]
		# Sinon:
		else:
			# On avance jusqu'à la prochaine balise.
			text = text[1:]
	# On vérifie que la pile est vide à la fin (au cas où il y aurait des balises ouvrantes de trop)
	return len(tag_stack) == 0


if __name__ == "__main__":
	brackets = ("(", ")", "{", "}", "[", "]")
	yeet = "(yeet){yeet}"
	yeeet = "({yeet})"
	yeeeet = "({yeet)}"
	yeeeeet = "(yeet"
	print(check_brackets(yeet, brackets))
	print(check_brackets(yeeet, brackets))
	print(check_brackets(yeeeet, brackets))
	print(check_brackets(yeeeeet, brackets))
	print()

	spam = "Hello, world!"
	eggs = "Hello, /* OOGAH BOOGAH world!"
	parrot = "Hello, OOGAH BOOGAH*/ world!"
	dead_parrot = "Hello, /*oh brave new */world!"
	print(remove_comments(spam, "/*", "*/"))
	print(remove_comments(eggs, "/*", "*/"))
	print(remove_comments(parrot, "/*", "*/"))
	print(remove_comments(dead_parrot, "/*", "*/"))
	print()

	otags = ("<head>", "<body>", "<h1>")
	ctags = ("</head>", "</body>", "</h1>")
	print(get_tag_prefix("<body><h1>Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("<h1>Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("</h1></body>", otags, ctags))
	print(get_tag_prefix("</body>", otags, ctags))
	print()

	spam = (
		"<html>"
		"  <head>"
		"    <title>"
		"      <!-- Ici j'ai écrit qqch -->"
		"      Example"
		"    </title>"
		"  </head>"
		"  <body>"
		"    <h1>Hello, world</h1>"
		"    <!-- Les tags vides sont ignorés -->"
		"    <br>"
		"    <h1/>"
		"  </body>"
		"</html>"
	)
	eggs = (
		"<html>"
		"  <head>"
		"    <title>"
		"      <!-- Ici j'ai écrit qqch -->"
		"      Example"
		"    <!-- Il manque un end tag"
		"    </title>-->"
		"  </head>"
		"</html>"
	)
	parrot = (
		"<html>"
		"  <head>"
		"    <title>"
		"      Commentaire mal formé -->"
		"      Example"
		"    </title>"
		"  </head>"
		"</html>"
	)
	tags = ("html", "head", "title", "body", "h1")
	comment_tags = ("<!--", "-->")
	print(check_tags(spam, tags, comment_tags))
	print(check_tags(eggs, tags, comment_tags))
	print(check_tags(parrot, tags, comment_tags))
	print()

