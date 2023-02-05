from dataclasses import dataclass


@dataclass
class Xkcd:
    num: int | None = None
    title: str | None = None
    img: str | None = None
    should_skip: bool | None = None

    def __str__(self):
        return f"→ num: {self.num} / title: {self.title} / img: {self.img}"
