from collections.abc import Collection
from random import Random

from hypothesis import example, given
from hypothesis.strategies import booleans, composite, integers, randoms, text
from pytest import mark

from miscellaneous_python.anagrams import anagram_checker
from tests.shared_strategies import Draw, latin_letter_strategy, non_letter_strategy

Strings: type[Collection] = Collection[str]


@composite
def strings_generator(draw: Draw) -> Strings:
    result: list[str] = []
    base_phrase: str = draw(text(latin_letter_strategy, min_size=2))
    randomizer: Random = draw(randoms())

    def swap_case(letter: str) -> str:
        return letter.swapcase() if draw(booleans()) else letter

    most_anagrams_possible: int = 11
    word_count: int
    for word_count in range(draw(integers(2, most_anagrams_possible))):
        group: list[str] = [
            *map(swap_case, base_phrase),
            *draw(text(non_letter_strategy)),
        ]
        randomizer.shuffle(group)

        result.append("".join(group))

    return result


@given(strings_generator())
@example(("Silent", "Listen"))
@example(("Anagram", "Nag a ram"))
@example(("liter", "litre", "tiler"))
@example(("ArE", "eAr"))
def test_are_anagrams(are_anagrams_params: Strings):
    assert anagram_checker(are_anagrams_params)


@mark.parametrize(
    "not_anagrams_params",
    (("where", "when"), ("nag", "Gram"), ("liter", "litre", "tiler", "peril")),
)
def test_not_anagrams(not_anagrams_params: Strings):
    assert not anagram_checker(not_anagrams_params)
