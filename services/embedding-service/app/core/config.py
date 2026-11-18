
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="EMBEDDING_",
        env_file=".env",
        extra="ignore",
    )

    # Service
    service_name: str = "embedding-service"

    # Model
    model_name: str = "BAAI/bge-m3"
    model_repo_id: str = "raludi/bge-m3-onnx-int8"
    model_dimension: int = Field(default=1024, gt=0)
    max_sequence_length: int = Field(default=512, gt=0)

    # Inference device
    device: Literal["cpu"] = "cpu"

    # ONNX Runtime
    intra_op_num_threads: int = Field(default=2, gt=0)
    inter_op_num_threads: int = Field(default=1, gt=0)
    execution_mode: Literal["sequential"] = "sequential"

    enable_cpu_mem_arena: bool = False
    enable_mem_pattern: bool = False

    graph_optimization_level: Literal["disable_all"] = "disable_all"


settings = Settings()
