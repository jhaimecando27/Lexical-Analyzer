from redef import reserved_words, reserved_symbols, let, symbols


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


def tokenize(program, str_pos, tmp_tokens, avoid):
    """Yung nangyayari dito, i-chcheck nya letter by letter yung input string
    tas icocompare nya yung letter sa same character position sa lahat ng words
    (e.g. reserved words) tas kapag hinde parehas tatanggalin nya yung word na
    yun sa isang list (tmp_tokens), gagawin nya yun hanggang isa or wala natira

    STATUS: reserved words and symbols palang

    TODO:
        - Respect delimeter

    Params:
        program     - (STR) 1 line of code
        str_pos     - (INT) current charactor position in the program
        tmp_tokens  - (DICT) list of tokens (Reserved Words/Symbols)
        avoid       - (SET) list of char that should not be in word


    Returns:
        result - Two dimentional array (lexem, token)
    """
    # Char position for token
    token_pos = 0

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

    print(program)

    while True:
        if program[str_pos] == " ":
            str_pos += 1

        # Reserved Symbols
        if program[str_pos] in symbols:
            result, str_pos = tokenize(program, str_pos, tmp_tokens_rs, avoid=let)
            results.append(result)
            tmp_tokens_rs.update(reserved_symbols)

        # Reserved Words
        elif program[str_pos] in let:
            result, str_pos = tokenize(program, str_pos, tmp_tokens_rw, avoid=symbols)
            results.append(result)
            tmp_tokens_rw.update(reserved_words)

        print(str_pos)
        if str_pos == len(program):
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
            text = text[:start_index] + text[end_index + len(end_pattern) :]
        else:
            break

    return text


def error_check(prog):
    pass
