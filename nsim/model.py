class Model:
    """
    Represents anything with an ID
    """

    __id: str

    def __init__(self, id: str) -> None:
        self.__id = id

    def get_id(self) -> str:
        return self.__id
