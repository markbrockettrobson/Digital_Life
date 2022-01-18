from digital_Life.interface.i_sample import ISample


class Sample(ISample):
    @staticmethod
    def add_one(value: int) -> int:
        return value + 1
