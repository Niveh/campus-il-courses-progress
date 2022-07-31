

class MusicNotes:
    def __init__(self) -> None:
        self._notes = [55, 61.74, 65.41, 73.42, 82.41, 87.31, 98]
        self._index = -1
        self._multi = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._notes) - 1:
            self._multi *= 2
            if self._multi > 16:
                raise StopIteration()

            self._index = -1

        self._index += 1
        return self._notes[self._index] * self._multi


notes_iter = iter(MusicNotes())

for freq in notes_iter:
    print(freq)
