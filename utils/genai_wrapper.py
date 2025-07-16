import dataclasses as dc
from typing import Literal, Union, List, Optional

from utils.config import get_config
from utils.logger import logger

ModelType = Union[Literal['chat'], Literal['embedding']]

@dc.dataclass(frozen=True)
class ModelConfig:
    model_name: str
    type: ModelType = 'chat'

    @property
    def display(self) -> str:
        return self.model_name

    def genai_params(self) -> dict:
        params = {'model': self.model_name}
        return params

@dc.dataclass(frozen=True)
class WrapperConfig:
    base_url: str
    api_key: str
    models: List[ModelConfig] =  dc.field(default_factory=list)

    def params(self, key_prefix: str = '') -> dict:
        params = {
            f'{key_prefix}base_url': self.base_url,
            f'{key_prefix}api_key': self.api_key,
        }
        return params

    def available_models(self, genai_model_type: Optional[ModelType]) -> list[ModelConfig]:
        return [ m for m in self.models if m.type == genai_model_type ]

    def get_model(self, model_name: str, genai_model_type: Optional[ModelType]) -> ModelConfig:
        lookup = { m.model_name: m for m in self.available_models(genai_model_type=genai_model_type)}
        if model_name in lookup:
            return lookup[model_name]
        else:
            raise Exception(f'Model: {model_name} not found!!')

def global_genai_config() -> WrapperConfig:
    config = get_config()
    return WrapperConfig(base_url=config['genai']['base_url'],
                         api_key=config['genai']['api_key'],
                         models=[ModelConfig(**m) for m in config['genai']['models']])

if __name__ == '__main__':
    genai_config = global_genai_config()
    logger.info(genai_config)
    logger.info(genai_config.get_model(genai_model_type='chat', model_name='deepseek-chat'))
    logger.info(genai_config.available_models(genai_model_type='embedding'))
