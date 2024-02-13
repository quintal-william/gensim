class Model:
    """
    Represents anything with an ID
    """

    __id: str

    def __init__(self, model_id: str) -> None:
        self.__id = model_id

    def get_id(self) -> str:
        return self.__id
