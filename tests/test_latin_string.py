from collections import Callable
from random import Random
from typing import TypeVar

from hypothesis import given, strategies

from auxiliary.latin_string import letter_filter, string_validator
from tests import shared_strategies

T = TypeVar("T")


@strategies.composite
def string_generator(
    draw: Callable[[strategies.SearchStrategy[T]], T],
    latin_only: bool = True,
    latin_count_min: int = 0,
) -> str:
    latin_letter_string: str = draw(
        strategies.text(
            shared_strategies.latin_letter_strategy, min_size=latin_count_min
        )
    )
    non_letter_string: str = draw(
        strategies.text(shared_strategies.non_letter_strategy)
    )

    result: str = latin_letter_string + non_letter_string

    if not latin_only:
        non_latin_string: str = draw(
            strategies.text(
                strategies.characters(
                    whitelist_categories=shared_strategies.LETTER_CATEGORY,
                    min_codepoint=shared_strategies.LOWER_Z_CODEPOINT + 1,
                ),
                min_size=1,
            )
        )
        result += non_latin_string

    sampler: Random = draw(strategies.randoms(note_method_calls=True))
    return "".join(sampler.sample(result, k=len(result)))


@given(string_generator(latin_count_min=1))
def test_valid_string(string: str) -> None:
    assert string_validator(string)


@given(string_generator(latin_only=False))
def test_invalid_string(string: str) -> None:
    assert not string_validator(string)


@given(strategies.data())
def test_latin_filter(data_strategy: strategies.DataObject) -> None:
    latin_count: int = data_strategy.draw(strategies.integers(min_value=1))
    drawn_string: str = data_strategy.draw(
        string_generator(latin_count_min=latin_count)
    )

    assert len(letter_filter(drawn_string)) >= latin_count