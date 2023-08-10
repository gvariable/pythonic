from typing import Any
import functools
import builtins


class Pipe:
    def __init__(self, function) -> None:
        self.function = function
        functools.update_wrapper(self, function)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return Pipe(
            lambda iterable, *args2, **kwargs2: self.function(
                iterable, *args, *args2, **kwargs, **kwargs2
            )
        )

    def __ror__(self, other):
        return self.function(other)


@Pipe
def take(iterable, qte):
    "Yield qte of elements in the given iterable."
    for item in iterable:
        if qte > 0:
            qte -= 1
            yield item
        else:
            return


@Pipe
def step_by(iterable, step):
    "Yield one item out of 'step' in the given iterable."
    for i, item in builtins.enumerate(iterable):
        if i % step == 0:
            yield item


@Pipe
def position(iterable, predicate):
    "Get the position of the element in the iterable."
    for i, item in builtins.enumerate(iterable):
        if predicate(item):
            return i


"Apply the given function to each item of the iterable."
map = Pipe(lambda iterable, predicate: builtins.map(predicate, iterable))
"Filter the given iterable using the given predicate."
filter = Pipe(lambda iterable, predicate: builtins.filter(predicate, iterable))
"Reduce the given iterable to one element using the given criterion."
reduce = Pipe(lambda iterable, predicate: functools.reduce(predicate, iterable))
"Collect the given iterable using the given collector."
collect = Pipe(lambda iterable, collector: collector(iterable))
"Enumerate the given iterable."
enumerate = Pipe(lambda iterable, start=0: builtins.enumerate(iterable, start))
"Zip the given iterable."
zip = Pipe(lambda iterable, *iterables: builtins.zip(iterable, *iterables))

if __name__ == "__main__":
    keys = range(10) | step_by(2) | map(lambda x: str(x) * 5) | collect(list)
    vals = range(10) | take(5) | enumerate(-5) | collect(list)
    d = keys | zip(vals) | collect(dict)
    print(d)
