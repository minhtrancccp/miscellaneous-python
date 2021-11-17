from typing import Literal

from beartype import beartype


def _increment_decrement(sign: Literal["+", "-", ">", "<"]) -> int:
    return -1 if sign in ["-", "<"] else 1


class Computer:
    @beartype
    def __init__(self, memory_size: int) -> None:
        self.pointer: int = 0

        if memory_size < 1:
            raise ValueError(f"{memory_size} -> Memory size must be a positive integer")

        self.memory: list = [0] * memory_size

    @beartype
    def action_choosing(
        self, input_sign: Literal["+", "-", ">", "<", "[", "]", ".", ","]
    ) -> None:
        if input_sign in ["+", "-"]:
            return self.delta_memory(input_sign)

        elif input_sign in [">", "<"]:
            return self.delta_pointer(input_sign)

        elif input_sign == ".":
            return self.get_char()

        elif input_sign == ",":
            return self.put_char()

    def delta_memory(self, memory_sign: Literal["+", "-"]) -> None:
        self.memory[self.pointer] += _increment_decrement(memory_sign)

    def delta_pointer(self, pointer_sign: Literal[">", "<"]) -> None:
        self.pointer += _increment_decrement(pointer_sign)

    def get_char(self) -> None:
        print(chr(self.memory[self.pointer]), end="")

    def put_char(self) -> None:
        ...