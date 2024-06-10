from pydantic_settings import BaseSettings

from src.utilities.singleton import singleton


@singleton
class Environment(BaseSettings):
    ENVIRONMENT: str = 'production'

    HOST_IP: str
    CONTAINER_PORT: int
    COMPOSE_PROJECT_NAME: str

    TRAIN_DATA_PATH: str
