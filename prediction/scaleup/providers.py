"""Provider routing scoped to this dataset; historical shared registry is unchanged."""
from dataclasses import asdict, replace

from prediction.client import configurations as legacy_configurations, ModelConfig

OPENROUTER_ROUTES = {
    "qwen-3.8-27b": "qwen/qwen3.8-27b",
    "glm": "z-ai/glm-5.3",
    "kimi-k3": "moonshotai/kimi-k3",
}


def configurations(names, provider="openrouter"):
    configs = legacy_configurations(names)
    if provider == "configured":
        return configs
    if provider != "openrouter":
        raise ValueError("Unknown routing policy")
    for name, value in configs.items():
        if value["provider"] == "openrouter":
            continue
        if name not in OPENROUTER_ROUTES:
            raise ValueError("No verified OpenRouter route for "+name)
        configs[name] = asdict(replace(ModelConfig(**value), provider="openrouter",
            provider_model=OPENROUTER_ROUTES[name], base_url="https://openrouter.ai/api/v1", key_env="OPENROUTER_API_KEY"))
    return configs
