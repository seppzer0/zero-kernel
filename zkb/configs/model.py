from pydantic import BaseModel, ConfigDict


class ModelConfig(BaseModel):
    """Model configuration."""
    model_config = ConfigDict(extra="forbid")
