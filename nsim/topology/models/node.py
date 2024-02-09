class Node:
    """
    Represents anything that can be (sub-)connected to anything
    """

    __name: str

    def __init__(self, name: str) -> None:
        self.__name = name
    
    def get_name(self) -> str:
        return self.__name
    
