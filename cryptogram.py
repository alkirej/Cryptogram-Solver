"""
File:    cryptogram.py
Author:  Jeff Alkire
Date:    February 2023
Purpose: Module to create and/or solve cryptograms.
"""
import random
import string
import sys

from collections import Counter

_DEBUG = True
_SAMPLE_GRAMS = ["Xesmzdhmbebj nwramj tnqjazy qxuejj maz xedhbmzu'j xesjenz. "
                 + "- Awmxaawfzu'j Rbwyz me maz Rqnqcp",
                 "Svg xvbcg hebycgj xdsv svg xbecq di svls rbbci lkq rlklsdwi "
                 + "leg lcxlpi ib wgesldk br svgjigcfgi, yos xdige hgbhcg ib rocc "
                 + "br qboysi. - Ygeselkq Eoiigcc",
                 "Xkdn fgknc qhu fczch ycqnf qtk kdn xqvjcnf rnkdtjv xknvj kh vjlf gkhvlhchv, "
                 + "q hci hqvlkh, gkhgclzcu lh Olrcnvy, qhu uculgqvcu vk vjc pnkpkflvlkh vjqv "
                 + "qoo sch qnc gncqvcu cmdqo.",
                 "V mvxegc nk v rgiizh hyz igxdk pzq ynk qlmcgiiv hygx ayg kqx nk kynxnxo vxd "
                 + "hvxak na mvue ayg lnxqag na mgonxk az cvnx.- Lvce Ahvnx",
                 "E lhcnsml efo isso vxndslsvxnked ascb ksmdo yh acnwwhf ksflnlwnfi "
                 + "hfwnchdj sg psbhl.",
                 "Wzb eit uaytx zw xfd fx vtaei, hke eit yfwe zw yzv fx tetbdal lfwt "
                 + "fd jibfxe otxkx zkb lzbv",
                 "P jnpyk mipga shlx. Jna necix hia teez, lec gaaj h bej ev pyjaiaxjpyt "
                 + "saesba, lec jihdab h bej.",
                 "Fkl nbpvyswn gwqew bh vihswlhh yqqgh esfk bihflul jshdboqu itqw fkl "
                 + "vihswlhh gwqew bh nbpvyswn.",
                 "Rm lphgmemw lpw hlaw, grmcrme rm tm l happme je pj, A ipjg pjc: jpm "
                 + "crapy A ipjg, crlc, grmemlh A glh txapw, pjg A hmm.",
                 "Ma wnq ilw gxr igeo g jgi gzgli in koo pnc mi cnlek, ipo amlki ipmxt "
                 + "wnq pgyo nx wnql pgxrk mk g xnxcnlemxt jgi",
                 "Aqlcqrpj pmjf gd wquffdk slq adlatd fl qdrz, rkz lktn ukvuzdkfrttn "
                 + "slq prvhukdj fl dxdvmfd.",
                 "Ydi apccbnbxdfvi yklydnxk fxnudjvjei ba bdkbafbdepbauywvx chjo oyebn.",
                 ]


_MOST_COMMON_LETTERS = ['e', 't', 'a', 'o', 'n']
_MOST_COMMON_PAIRS = ['th', 'he', 'an', 're', 'er']
_MOST_COMMON_DOUBLES = ['ll', 'ee', 'ss', 'oo', 'tt']

_WORD_FILE = "words_alpha.txt"
# _WORD_FILE = "/usr/share/dict/american-english"

# define GLOBAL _WORD_LIST set for use in this module only
with open(_WORD_FILE, "r", encoding="utf-8") as fd:
    _WORD_LIST = set(fd.read().lower().split())


def is_english_word(word: str) -> bool:
    """
    Determine if a word is English by looking into the word list file and
    looking for it.

    param word:  Word to look up
    return:      true/false if file is/is not in the english word list
    """
    return word.lower() in _WORD_LIST


def word_template(word: str) -> str:
    """
    Convert an english word into a template. A template is a string starting
    with the letter a that uses a new letter for each different letter found in
    the string.  If a duplicate letter is found in the word, the same letter
    is substituted in the word.

    Example:
        apple -> abbcd
        encyclopedia -> abcdcefgahij

    param word:
    return:
    """
    letter_map = {}
    template_ltr = 'a'

    for ltr in word.lower():
        if ltr not in letter_map:
            letter_map[ltr] = template_ltr
            template_ltr = chr(ord(template_ltr) + 1)

    return_value = []
    for ltr in word.lower():
        return_value.append(letter_map[ltr])

    return ''.join(return_value)


def build_word_templates(word_list: list = None) -> dict:
    """
    Given a list of words, create a word template for each word and store them in
    a dictionary using the template as a lookup.  The lookup value will be a list
    of items that match the template (or None if none exists)

    param word_list:  list of words to build templates for
    return:           a dictionary that uses the word templates as the key
                        and a list of words from the list matching the template.
    """
    if word_list is None:
        word_list = _WORD_LIST

    char_templates = {}  # templates

    for word in word_list:
        tmpl = word_template(word)     # templates

        if tmpl in char_templates:
            char_templates[tmpl].append(word)
        else:
            char_templates[tmpl] = [word]

    return char_templates


_WORD_TEMPLATES = build_word_templates()


def possible_decrypt_values(template: str) -> dict:
    """
    Given a word template,

    param t: word template to work with
    return:  dictionary of all possible values for a given letter in the word.
    """
    try:
        tmpl = word_template(template.lower())
        decrypt_options = {}

        possible_words = _WORD_TEMPLATES[tmpl]

        for idx, ltr in enumerate(template.lower()):
            for wrd in possible_words:
                add_to_valids(decrypt_options, ltr, wrd[idx])

        return decrypt_options

    # Cannot fine template.  Typo or a name, etc.
    except KeyError:
        return {}


def intersect_possibles(*args: dict) -> dict:
    """
    Given a list of possible decryptions, find values that will work for all
    items in the list.

    param ps: list of possible decryption value dictionaries
    return:   a possible decryption value dictionary with values that would work
                 for all words in the list.
    """
    final_possibles = {}

    for arg in args:
        for ltr, poss in arg.items():
            if ltr in final_possibles:
                final_possibles[ltr] = final_possibles[ltr] & poss
            else:
                final_possibles[ltr] = poss

    return final_possibles


def union_possibles(*args: dict) -> dict:
    """
    Given a list of possible decryptions, find values that will work for all
    items in the list.

    param ps: list of possible decryption value dictionaries
    return:   a possible decryption value dictionary with values that would work
                 for all words in the list.
    """
    final_possibles = {}

    for arg in args:
        for ltr, poss in arg.items():
            if ltr in final_possibles:
                final_possibles[ltr] = final_possibles[ltr] | poss
            else:
                final_possibles[ltr] = poss

    return final_possibles


def prune_empties(possibles: dict) -> dict:
    """
    Remove any dictionary values containing all characters.  This is the same
    meaning as an empty list.

    param possibles: dictionary containing lists of possible decryption options.
    return:  updated possibles dictionary
    """
    remove_letters = []
    for ltr in possibles:
        if len(string.ascii_lowercase) == len(possibles[ltr]):
            remove_letters.append(ltr)

    for ltr in remove_letters:
        possibles.pop(ltr)
    return possibles


def add_to_valids(valids: dict, ltr_enc: str, ltr_valid: str) -> dict:
    """
    Add a given decryption possibility to the list

    param valids: the current possible decryption values.  A list for each letter.
    param ltr_enc: the encrypted value of the letter.
    param ltr_valid: the possible decryption value of the letter.
    return: a new, updated dictionary of possible decryption values.
    """
    possible_enc = valids.get(ltr_enc.lower(), set())
    possible_enc.add(ltr_valid.lower())
    valids[ltr_enc] = possible_enc

    return valids


def match_case(ltr_to_match: str, ltr: str) -> str:
    """
    Convert ltr to the same case as ltr_to_match.

    param ltr_to_match: a character whose case will be matched
    param ltr: the letter to return in the appropriate case
    return: ltr in upper or lowercase depending on ltr_to_match
    """
    if ltr_to_match[0] in string.ascii_uppercase:
        return ltr.upper()

    return ltr.lower()


def build_answer(cryptogram: str, ltr_filter: dict) -> str:
    """
    Create the decrypted cryptogram

    param cryptogram: original cryptogram
    param ltr_filter: dictionary of possible decryption values
    return: a string with the (near) answer
    """
    result = []
    for idx, ltr in enumerate(cryptogram.lower()):
        if ltr not in string.ascii_lowercase:
            result.append(ltr)
            continue

        answer_letters = ltr_filter.get(ltr, {'*'})
        if len(answer_letters) > 1:
            result.append('[')

        if len(answer_letters) > 5:
            result.append(str(len(answer_letters)))
        else:
            for item in answer_letters:
                item = match_case(cryptogram[idx], item)
                result.append(item)
        if len(answer_letters) > 1:
            result.append(']')

    return ''.join(result)


def clean_known(valids: dict) -> dict:
    """
    Remove any letters that are completly solved from all other
    possibles.

    param valids: the dictionary of possible decryption values
    return: the updated possible decrypt values dictionary
    """
    singles = {}
    for key, val in valids.items():
        if len(val) == 1:
            singles[key] = list(val)[0]

    for key, val in valids.items():
        if key in singles:
            continue

        for ltr in singles.values():
            try:
                val.remove(ltr)
                valids[key] = val
            except KeyError:
                pass

    return valids


def prune(word: str, valids: dict) -> dict:
    """
    Remove any values from the possible decryption values dictionary
    that are not possible for the supplied (encrypted) word.

    param word: the encrypted word
    param valids: the dictionary of possible decryption values
    return: the updated possible decrypt values dictionary
    """
    std_template = word_template(word.lower())
    matches = _WORD_TEMPLATES.get(std_template, {})
    valid_for_word: dict = {}

    for current_match in matches:
        valid_for_match: dict = {}

        for index, _ in enumerate(current_match):
            ltr_encr = word[index]
            ltr_valid = valids.get(ltr_encr, set())

            ltr_mtch = current_match[index]

            if 0 == len(ltr_valid) or ltr_mtch in ltr_valid:
                valid_for_match = add_to_valids(valid_for_match, ltr_encr, ltr_mtch)
            else:
                valid_for_match = {}
                break

        valid_for_word = union_possibles(valid_for_word, valid_for_match)

    return intersect_possibles(valids, valid_for_word)


def filter_size(letter_filter: dict) -> int:
    """
    Determine the "size" of the possible values dictionary. Smaller values
    are closer to the unique answer.

    param letter_filter: the dictionary of possible decryption values
    return: the sum of the number of possible decryption letters for each
            letter in the alphabet.
    """
    sze = 0
    for ltr in string.ascii_lowercase:
        options = letter_filter.get(ltr, '')
        if 0 == len(options):
            sze += len(string.ascii_lowercase)
        else:
            sze += len(options)

    return sze


def print_possibles(dct: dict) -> None:
    """
    Print the possible values dictionary in a compact way.  For debugging

    param dct: the possible values dictionary
    """
    if _DEBUG:
        print('     ', end='')
        for key, val in dct.items():
            print(key.upper(), end=':')
            for ltr in sorted(val):
                print(ltr, end='')
            print(',  ', end='')

        print()


def solve_cryptogram(gram: str, valids: dict) -> str:
    """
    Given a cryptogram, attempt to solve it.

    param gram: The original cryptogram
    return: The answer or near answer as a string
    """
    words = gram.lower().translate(str.maketrans('', '', string.punctuation)).split()
    decryption_possibilities = valids

    new_sz = filter_size(decryption_possibilities)
    old_sz = new_sz + 1

    while new_sz < old_sz:
        old_sz = new_sz

        decryption_possibilities = clean_known(decryption_possibilities)
        for word in words:
            decryption_possibilities = prune(word, decryption_possibilities)

        new_sz = filter_size(decryption_possibilities)

    return build_answer(gram, decryption_possibilities)


def grade_solution(result: str) -> (int, int):
    """
    Grade the cryptogram solution. A grade has two parts:
        Part 1 = the sum of the number of possible choices for all letters
                    that have more than 1 potential value.
        Part 2 = the number of valid english words found in the answer

    param result: the cryptogram solution to be graded
    return: The grade for the solution (see fn description).
    """
    # Check for unknown values
    cnt_mode = False
    ttl_cnt, crt_cnt = 0, 0

    for ltr in result:
        if cnt_mode:
            if ']' == ltr:
                cnt_mode = False
                ttl_cnt += crt_cnt
            else:
                if ltr.isdigit():
                    crt_cnt *= 10
                    crt_cnt += int(ltr)
                else:
                    crt_cnt += 1
        else:
            if '*' == ltr:
                crt_cnt += 26
            elif '[' == ltr:
                cnt_mode = True
                crt_cnt = 0

    # check for english words.

    wrd_cnt = 0
    words = result.lower().translate(str.maketrans('', '', string.punctuation)).split()
    for word in words:
        if is_english_word(word):
            wrd_cnt += 1

    # first value is # of possibilities not decrypted.
    # second value is the number of valid english words found
    return ttl_cnt, wrd_cnt


def is_better(score1: (int, int), score2: (int, int)):
    """
    Compare the grades (see grade_grade_solution) of two solutions.
    Note: a solution has 2 parts.
            Part 1 = number of choices for unknown letters.
            Part 2 = number of valid english words found.

    param score1: the score of the first solution
    param score2: the score of the second solution
    return: True if the first solition is a better solution, False if the
                second solution is better (or if the solutions received
                the same grade).
    """
    if score1[1] == score2[1]:
        return score1[0] < score2[0]
    return score1[1] > score2[1]


def all_letter_pairs(phrase: str) -> list:
    """
    Get a list of all letter pairs in the supplied phrase.

    param phrase: Cryptogram phrase
    return: A list of all contiguous letters in the phrase.  Contiguous letters
            must be in the same word. Duplicates are intentionally NOT REMOVED.
    """
    all_pairs = []
    words = phrase.split()
    for word in words:
        for idx in range(len(word)-2):
            if word[idx] in string.ascii_lowercase and word[idx+1] in string.ascii_lowercase:
                ltr_pair = word[idx:idx+2]
                all_pairs.append(ltr_pair)

    return all_pairs


def most_common_letter_pairs(gram: str, count: int = 5) -> list:
    """
    Find the most common pairs of contiguous letters in the cryptogram.

    param gram: Phrase to parse for the letter pairs.
    param count: The number of letter pairs desired.
    return: Up to the first <count> pairs of letters that occur the most times
            in the phrase.  NOTE: Double letters are always returned even if
            the list exceeds <count>.
    """
    mc_pairs = []
    all_pairs = all_letter_pairs(gram)

    counts = Counter(all_pairs)
    srt_quan = sorted(counts.items(), key=lambda item: item[1], reverse=True)

    for idx, pair in enumerate(srt_quan):
        if idx < count or pair[0][0] == pair[0][1]:
            mc_pairs.append(pair[0])

    return mc_pairs


def one_letter_words(phrase: str) -> set:
    """
    Find the set of one letter words in this phrase

    param phrase: the cryptogram to search through for single letter words
    return: a set of the one character words in the phrase.
    """
    results = set()
    for word in phrase.split():
        if len(word) == 1:
            results.add(word)

    return results


def most_used_letters(gram: str, count: int = 5) -> list:
    """
    Return the <count> most common letters in <gram>.

    param gram: cryptogram to check letter frequency for.
    param count: the number of letters to return
    return: sorted list of most common letters in <gram> starting with
                the most frequently used letter.
    """
    counts = Counter(gram.lower())
    freqs = []

    srt_quan = sorted((counts.items()), key=lambda item: item[1], reverse=True)
    found = 0

    for ltr, _ in srt_quan:
        if ltr in string.ascii_lowercase:
            found += 1
            if found > count:
                break
            freqs.append(ltr)

    return freqs


def find_best_solution_with_hints(gram: str, hints_lst: list = None) -> ((int,int),str):
    """
    Receive a list of hints (Hints are starting valids dictionaries). Solve
    the cryptogram with each of the hint sets in the list, determine which
    is best, and return the solution and its associated score.

    param gram: Cryptogram to solve
    param hints_lst: List of dictionaries where each dictionary is the starting
                     selection of valid letters.
    return: Tuple of the solution's score and the solution.
    """
    best_ans, best_sco = None, None
    if hints_lst is None:
        hints_lst = [{}]

    for hints in hints_lst:
        ans = solve_cryptogram(gram, hints)
        sco = grade_solution(ans)
        if (best_ans is None) or (is_better(sco, best_sco)):
            best_ans = ans
            best_sco = sco

    return best_sco, best_ans

def find_best_solution(gram: str) -> str:
    """
    Solve the supplied cryptogram.  Solve it many times supplying some
    hints as to the expected solution based on letter frequencies and
    other criteria.  Return the best answer out of all attempts.

    param gram: The cryptogram to solve
    return: The best solution.
    """
    hints_list = [{}]

    # Use letter frequency as a starting place
    freqs = most_used_letters(gram)
    for encr in freqs:
        for english in _MOST_COMMON_LETTERS:
            decrypt_key = {}
            add_to_valids(decrypt_key, encr, english)
            hints_list.append(decrypt_key)

    # Use most frequent sequential letters in English as hints.
    freqs = most_common_letter_pairs(gram)
    for encr_pair in freqs:
        # choose proper pair list (double letters or not)
        if encr_pair[0] == encr_pair[1]:
            pair_list = _MOST_COMMON_DOUBLES
        else:
            pair_list = _MOST_COMMON_PAIRS

        for eng_pair in pair_list:
            decrypt_key = {}
            add_to_valids(decrypt_key, encr_pair[0], eng_pair[0])
            add_to_valids(decrypt_key, encr_pair[1], eng_pair[1])
            hints_list.append(decrypt_key)

    # Try A or I for single letter words.
    for one_letter_word in one_letter_words(gram):
        for ltr in ['a','i']:
            decrypt_key = {}
            add_to_valids(decrypt_key, one_letter_word, ltr)
            hints_list.append(decrypt_key)

    return find_best_solution_with_hints(gram, hints_list)[1]


def create_cryptogram(txt: str) -> str:
    """
    Create a cryptogram from a given text.

    param txt: Original text
    return: Cryptogram text
    """
    enc_dict: dict = {}
    unused = list(string.ascii_lowercase)

    for ltr in string.ascii_lowercase:
        enc_ltr = random.choice(unused)
        unused.remove(enc_ltr)
        enc_dict[ltr] = [enc_ltr]

    return build_answer(txt, enc_dict)


def main() -> int:
    """
    Main routine for the solve cryptogram program.

    return: 0 upon successful run, other value for a failure.
    """
    # Determine the cryptogram to solve (a supplied one or a sample one)
    if len(sys.argv) > 1:
        solve_me = ' '.join(sys.argv[1:])
    else:
        solve_me = random.choice(_SAMPLE_GRAMS)

    print()
    print("CRYPTOGRAM:")
    print("     ", end='')
    print(solve_me)
    print()

    answer = find_best_solution(solve_me)
    print("RESULT:")
    print("     ", end='')
    print(answer)
    print()

    return 0


if __name__ == "__main__":
    main()
