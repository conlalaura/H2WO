from dataclasses import dataclass


@dataclass
class Review:
    username: str
    rating: int
    comment: str

    def __post_init__(self):
        if not (1 <= self.rating <= 5):
            raise ValueError(f"Rating must be between 1 and 5. Got: {self.rating}")
