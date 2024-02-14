from nsim.generator import Generator

from .poisson import PoissonTrafficGenerator
from .constant import ConstantTrafficGenerator
from .train import TrainTrafficGenerator
from ..models.traffic import Traffic


traffic_generators: dict[str, Generator[Traffic]] = {
    "constant": ConstantTrafficGenerator(),
    "poisson": PoissonTrafficGenerator(),
    "train": TrainTrafficGenerator(),
}
