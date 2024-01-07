from redef import (
    reserved_words, reserved_symbols,
    let, symbols, diglet,
    delimi, delims, delimb, dig, delimtf
)


def test(tmp_tokens, char, token_pos, str_pos, token):
    """for testing purposes only"""
    print(
        "tmp: "
        + str(len(tmp_tokens))
        + " | char: "
        + char
        + " | token_pos: "
        + str(token_pos)
        + " | str_pos: "
        + str(str_pos)
        + " Token: "
        + token
    )


def token_rw(program, str_pos, tmp_tokens, avoid):
    # Char position for token
    token_pos = 0
    result = []

    # Check if one of the reserved words
    while program[str_pos] != " " and program[str_pos] != "\n":
        # Check for disturbance
        if program[str_pos] in avoid:
            # TEST
            test(tmp_tokens, program[str_pos], token_pos, str_pos, token)

            # Add result
            result = (
                ("unknown", "unknown")
                if len(tmp_tokens) == 0
                else (
                    list(tmp_tokens.keys())[0],
                    list(tmp_tokens.values())[0],
                )
            )

            return result, str_pos

        # Loop through tokens using the current character
        for token in list(tmp_tokens):
            # TEST
            test(tmp_tokens, program[str_pos], token_pos, str_pos, token)

            if len(token) <= token_pos:
                tmp_tokens.pop(token)
                continue

            if token[token_pos] != program[str_pos]:
                tmp_tokens.pop(token)

        # Move to another letter
        token_pos += 1
        str_pos += 1

    # TEST
    test(tmp_tokens, program[str_pos], token_pos, str_pos, token)

    # Add result
    result = (
        ("unknown", "unknown")
        if len(tmp_tokens) == 0
        else (list(tmp_tokens.keys())[0], list(tmp_tokens.values())[0])
    )
    str_pos += 1
    return result, str_pos


def lexical_analysis(program):
    """read the line of code character by character.

    Params:
        program     - (STR) 1 line of code

    Returns:
        results - Two dimentional array (lexem, token)
    """
    tmp_tokens_rw = {}
    tmp_tokens_rw.update(reserved_words)

    tmp_tokens_rs = {}
    tmp_tokens_rs.update(reserved_symbols)

    results = []

    str_pos = 0

    while True:
        if program[str_pos] == " ":
            results.append(("space", "reserve symbol"))
            str_pos += 1

        # Tint and flora
        if program[str_pos] == "0":
            num = ""
            num += program[str_pos]
            str_pos += 1
            if program[str_pos] == ".":
                num += program[str_pos]
                str_pos += 1

                if program[str_pos] in dig:
                    num += program[str_pos]
                    str_pos += 1
                    while program[str_pos] not in delimtf or len(num) < 12:
                        num += program[str_pos]

                        if program[str_pos + 1] in delimtf:
                            results.append((num, "flora lit"))
                            break
                        str_pos += 1
                    str_pos += 1
            else:
                results.append(("0", "tint"))
                str_pos += 1
        elif program[str_pos] in dig:
            num = ""
            num += program[str_pos]
            str_pos += 1
            while program[str_pos] not in delimtf or len(num) < 6:
                num += program[str_pos]

                if program[str_pos + 1] in ".":
                    break

                if program[str_pos + 1] in delimtf:
                    results.append((num, "tint lit"))
                    break
                str_pos += 1
            str_pos += 1

            if program[str_pos] == ".":
                num += program[str_pos]
                str_pos += 1

                if program[str_pos] in dig:
                    num += program[str_pos]
                    str_pos += 1
                    while program[str_pos] not in delimtf or len(num) < 12:
                        num += program[str_pos]

                        if program[str_pos + 1] in delimtf:
                            results.append((num, "flora lit"))
                            break
                        str_pos += 1
                    str_pos += 1

        elif program[str_pos] == "-":
            num = ""
            num += program[str_pos]
            str_pos += 1

            if program[str_pos] in dig:
                num += program[str_pos]
                str_pos += 1
                while program[str_pos] not in delimtf or len(num) < 6:
                    num += program[str_pos]

                    if program[str_pos + 1] in ".":
                        break

                    if program[str_pos + 1] in delimtf:
                        results.append((num, "tint"))
                        break
                    str_pos += 1
                str_pos += 1

                if program[str_pos] == ".":
                    num += program[str_pos]
                    str_pos += 1

                    if program[str_pos] in dig:
                        num += program[str_pos]
                        str_pos += 1
                        while program[str_pos] not in delimtf or len(num) < 12:
                            num += program[str_pos]

                            if program[str_pos + 1] in delimtf:
                                results.append((num, "flora lit"))
                                break
                            str_pos += 1
                        str_pos += 1

        # Bloom
        if program[str_pos] == "t":
            str_pos += 1
            if program[str_pos] == "r":
                str_pos += 1
                if program[str_pos] == "u":
                    str_pos += 1
                    if program[str_pos] == "e" and program[str_pos + 1] in delimb:
                        results.append(("true", "bloom"))
                        str_pos += 1

        # Bloom
        if program[str_pos] == "f":
            if program[str_pos + 1] == "a":
                str_pos += 1
                if program[str_pos + 2] == "l":
                    str_pos += 1
                    if program[str_pos] == "s":
                        str_pos += 1
                        if program[str_pos] == "e" and program[str_pos + 1] in delimb:
                            results.append(("false", "bloom"))
                            str_pos += 1

        # Reserved Symbols
        if program[str_pos] in symbols:
            result, str_pos = token_rw(
                program, str_pos, tmp_tokens_rs, avoid=let)
            results.append(result)
            tmp_tokens_rs.update(reserved_symbols)

        # Reserved Words
        elif program[str_pos] in let:
            result, str_pos = token_rw(
                program, str_pos, tmp_tokens_rw, avoid=symbols)
            results.append(result)
            tmp_tokens_rw.update(reserved_words)

        # Identifier
        elif program[str_pos] == "#":
            identifier = ""

            results.append(("#", "reserve symbol"))
            str_pos += 1

            identifier += program[str_pos]
            str_pos += 1
            if program[str_pos] in let or program[str_pos + 1] in delimi:

                if program[str_pos] not in delimi:
                    identifier += program[str_pos]
                    str_pos += 1
                if program[str_pos] in diglet or program[str_pos + 1] in delimi:
                    if program[str_pos] not in delimi:
                        identifier += program[str_pos]
                        str_pos += 1
                    if program[str_pos] in diglet or program[str_pos + 1] in delimi:
                        if program[str_pos] not in delimi:
                            identifier += program[str_pos]
                            str_pos += 1
                        if program[str_pos] in diglet or program[str_pos + 1] in delimi:
                            if program[str_pos] not in delimi:
                                identifier += program[str_pos]
                                str_pos += 1
                            if program[str_pos] in diglet or program[str_pos + 1] in delimi:
                                if program[str_pos] not in delimi:
                                    identifier += program[str_pos]
                                    str_pos += 1
                                if program[str_pos] in diglet or program[str_pos + 1] in delimi:
                                    if program[str_pos] not in delimi:
                                        identifier += program[str_pos]
                                        str_pos += 1
                                    if program[str_pos] in diglet and program[str_pos + 1] in delimi:
                                        if program[str_pos] not in delimi:
                                            identifier += program[str_pos]
                                            str_pos += 1
                                        print("test")
            results.append((identifier, "identifier"))

        # String
        elif program[str_pos] == "\"":
            string = ""
            count = 0

            results.append(("\"", "reserve symbol"))
            str_pos += 1

            string += program[str_pos]
            str_pos += 1

            tmp = ""

            while program[str_pos] not in delims:
                string += program[str_pos]

                if program[str_pos + 1] in delims:
                    tmp = "\""
                    break
                str_pos += 1

            results.append((string, "string"))
            results.append((tmp, "reserve symbol"))

        if str_pos >= len(program):
            break

    return results


def ignore_comment(program):
    cleaned_text = remove_pattern(program, "<--", "-->")

    return cleaned_text


def remove_pattern(text, start_pattern, end_pattern):
    while True:
        start_index = text.find(start_pattern)
        end_index = text.find(end_pattern, start_index + len(start_pattern))

        if start_index != -1 and end_index != -1:
            text = text[:start_index] + text[end_index + len(end_pattern):]
        else:
            break

    return text


def error_check(prog):
    pass
