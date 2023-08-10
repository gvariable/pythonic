from typing import Any, List, Union
from abc import abstractclassmethod, ABC


class Runnable(ABC):
    def __or__(self, other: "Runnable") -> "RunnableSequence":
        return RunnableSequence(head=self, tail=other)

    def __ror__(self, other: "Runnable") -> "RunnableSequence":
        return RunnableSequence(head=other, tail=self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.run(*args, **kwds)

    @abstractclassmethod
    def run(self, *args: Any, **kwds: Any) -> Any:
        pass


class RunnableSequence(Runnable):
    def __init__(
        self, head: Runnable, tail: Runnable, middle: List[Runnable] = []
    ) -> None:
        self.head = head
        self.tail = tail
        self.middle = middle

    def __or__(self, other: Union[Runnable, "RunnableSequence"]) -> "RunnableSequence":
        if isinstance(other, Runnable):
            return RunnableSequence(
                head=self.head, middle=[*self.middle, self.tail], tail=other
            )
        elif isinstance(other, RunnableSequence):
            return RunnableSequence(
                head=self.head,
                middle=[*self.middle, self.tail, other.head, *other.middle],
                tail=other.tail,
            )

    def __ror__(self, other: Union[Runnable, "RunnableSequence"]) -> "RunnableSequence":
        if isinstance(other, Runnable):
            return RunnableSequence(
                head=other,
                middle=[self.head, *self.middle],
                tail=self.tail,
            )
        elif isinstance(other, RunnableSequence):
            return RunnableSequence(
                head=other.head,
                middle=[*other.middle, other.tail, self.head, *self.middle],
                tail=self.tail,
            )

    def __repr__(self) -> str:
        response = f"{repr(self.head)} | " + " | ".join([repr(m) for m in self.middle])
        response += f" | {repr(self.tail)}" if self.middle else repr(self.tail)
        return response

    def run(self, *args: Any, **kwds: Any) -> Any:
        retval = self.head(*args, **kwds)
        for runnable in [*self.middle, self.tail]:
            retval = runnable(retval)
        return retval


class ls(Runnable):
    def run(self, path) -> Any:
        return f"[ls {path}]"


class grep(Runnable):
    def run(self, path) -> Any:
        return f"[grep {path}]"


class wc(Runnable):
    def run(self, path) -> Any:
        return f"[wc {path}]"


command = ls() | grep() | wc()
print(command)
print(type(command))
print(command("/tmp/test.txt"))
