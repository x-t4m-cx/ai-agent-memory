import logging

import onnxruntime as ort
from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer

from app.core.config import settings


logger = logging.getLogger(__name__)


class ModelLoader:
    def __init__(self):
        self._tokenizer = None
        self._session = None

    @property
    def is_loaded(self) -> bool:
        return self._tokenizer is not None and self._session is not None

    @property
    def tokenizer(self):
        if self._tokenizer is None:
            raise RuntimeError("Tokenizer has not been loaded")
        return self._tokenizer

    @property
    def session(self):
        if self._session is None:
            raise RuntimeError("ONNX model has not been loaded")
        return self._session

    def load(self) -> None:
        if self.is_loaded:
            logger.info("Embedding model is already loaded")
            return

        logger.info("Loading tokenizer: %s", settings.model_repo_id)

        tokenizer = AutoTokenizer.from_pretrained(
            settings.model_repo_id,
        )

        logger.info("Downloading or locating ONNX model")

        model_path = hf_hub_download(
            repo_id=settings.model_repo_id,
            filename="onnx/model.onnx",
        )

        options = ort.SessionOptions()

        options.intra_op_num_threads = settings.intra_op_num_threads
        options.inter_op_num_threads = settings.inter_op_num_threads

        options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL

        options.enable_cpu_mem_arena = settings.enable_cpu_mem_arena
        options.enable_mem_pattern = settings.enable_mem_pattern

        options.graph_optimization_level = (
            ort.GraphOptimizationLevel.ORT_DISABLE_ALL
        )

        logger.info("Initializing ONNX Runtime session")

        session = ort.InferenceSession(
            model_path,
            sess_options=options,
            providers=["CPUExecutionProvider"],
        )

        output_names = {
            output.name: output
            for output in session.get_outputs()
        }

        if "sentence_embedding" not in output_names:
            raise RuntimeError(
                "ONNX model does not provide sentence_embedding output"
            )

        output_dimension = output_names["sentence_embedding"].shape[-1]

        if output_dimension != settings.model_dimension:
            raise RuntimeError(
                f"Unexpected embedding dimension: {output_dimension}. "
                f"Expected: {settings.model_dimension}"
            )

        self._tokenizer = tokenizer
        self._session = session

        logger.info(
            "Embedding model loaded successfully. Dimension: %s",
            settings.model_dimension,
        )
