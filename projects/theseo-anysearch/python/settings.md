# Settings Specification

## Design

Configuration is loaded from a YAML file. The top-level structure is **fixed** —
the same keys are always present regardless of which algorithm or model is used.
Lower-level sections (algorithm config, model config) are **configurable per
implementation** and validated against Pydantic models defined in `models.py`
(base) and subclassed in individual algorithm/model files.

```
YAML file
    │
    ▼
settings.py          loads and parses YAML, resolves which config classes to use
    │
    ├── models.py    base Pydantic models (top-level schema, fixed)
    │
    ├── rllib/algorithms/ppo.py     subclasses AlgorithmConfig for PPO-specific fields
    ├── rllib/algorithms/sac.py     subclasses AlgorithmConfig for SAC-specific fields
    │
    └── rllib/models/voxel_encoder.py   subclasses ModelConfig for its own fields
```

CLI flags override any YAML value at runtime (see `cli.md`).

---

## YAML File Structure

```yaml
# ── Top level: fixed, always present ──────────────────────────────────────────

env:
  stl_path: path/to/geometry.stl   # STL geometry to voxelize
  scale: 1.0                        # Voxelization scale factor
  agent_count: 4                    # Number of concurrent agents
  max_steps: 200                    # Steps per episode
  seed: 42                          # Global RNG seed

training:
  algorithm: ppo                    # Algorithm key (resolves to concrete AlgorithmConfig)
  model: voxel_encoder              # Model key (resolves to concrete ModelConfig)
  runner: local                     # Runner key: local | anyscale
  iterations: 100                   # RLlib training iterations
  checkpoint_interval: 10           # Iterations between checkpoints and GIF export
  output_dir: runtime/              # GIF and checkpoint output directory
  video_every: 10                   # Episodes between GIF frames

anyscale:
  cluster_env: theseo-cluster-env   # Anyscale cluster environment name
  compute_config: theseo-compute    # Anyscale compute config name
  project: theseo-anysearch         # Anyscale project name

# ── Lower levels: algorithm-specific and model-specific ───────────────────────

algorithm_config:                   # Validated against the class named by training.algorithm
  lr: 0.0003
  gamma: 0.99
  train_batch_size: 4096
  # PPO-specific:
  clip_param: 0.2
  num_sgd_iter: 10

model_config:                       # Validated against the class named by training.model
  hidden_sizes: [256, 256]
  activation: relu
  # voxel_encoder-specific:
  use_position_encoding: true
```

---

## `models.py` — Base Pydantic Models

Defines the fixed top-level schema and abstract base classes for lower-level sections.
All models use `model_config = ConfigDict(extra="forbid")` to catch unknown keys.

```python
class EnvConfig(BaseModel):
    stl_path: Path
    scale: float = 1.0
    agent_count: int = 4
    max_steps: int = 200
    seed: int = 42

class TrainingConfig(BaseModel):
    algorithm: str
    model: str
    runner: Literal["local", "anyscale"] = "local"
    iterations: int = 100
    checkpoint_interval: int = 10
    output_dir: Path = Path("runtime/")
    video_every: int = 10

class AnyscaleConfig(BaseModel):
    cluster_env: str
    compute_config: str
    project: str

class AlgorithmConfig(BaseModel):
    """Base for all algorithm-specific config sections. Subclassed per algorithm."""
    lr: float = 3e-4
    gamma: float = 0.99
    train_batch_size: int = 4096

class ModelConfig(BaseModel):
    """Base for all model-specific config sections. Subclassed per model."""
    hidden_sizes: list[int] = [256, 256]
    activation: Literal["relu", "tanh", "elu"] = "relu"

class Settings(BaseModel):
    """Root config object. Constructed by settings.py from the parsed YAML."""
    env: EnvConfig
    training: TrainingConfig
    anyscale: AnyscaleConfig
    algorithm_config: AlgorithmConfig   # resolved to concrete subclass at load time
    model_config: ModelConfig           # resolved to concrete subclass at load time
```

---

## Concrete Subclasses

Each algorithm and model implementation defines its own config class by subclassing
the relevant base. Fields in the subclass are algorithm/model-specific and only
appear when that implementation is selected.

### Example: `rllib/algorithms/ppo.py`

```python
class PPOConfig(AlgorithmConfig):
    clip_param: float = 0.2
    num_sgd_iter: int = 10
    lambda_: float = 0.95       # GAE lambda
    kl_coeff: float = 0.2
```

### Example: `rllib/models/voxel_encoder.py`

```python
class VoxelEncoderConfig(ModelConfig):
    use_position_encoding: bool = True
    encoder_depth: int = 3
```

---

## `settings.py` — Loader

`settings.py` is responsible for:
1. Reading the YAML file
2. Resolving `training.algorithm` → concrete `AlgorithmConfig` subclass
3. Resolving `training.model` → concrete `ModelConfig` subclass
4. Constructing and returning a validated `Settings` object

```python
# Registry: maps YAML key -> config class
ALGORITHM_CONFIGS: dict[str, type[AlgorithmConfig]] = {
    "ppo": PPOConfig,
    "sac": SACConfig,
}

MODEL_CONFIGS: dict[str, type[ModelConfig]] = {
    "voxel_encoder": VoxelEncoderConfig,
}

def load_settings(path: Path, overrides: dict = {}) -> Settings:
    raw = yaml.safe_load(path.read_text())
    deep_merge(raw, overrides)          # CLI flag overrides applied here

    algo_cls = ALGORITHM_CONFIGS[raw["training"]["algorithm"]]
    model_cls = MODEL_CONFIGS[raw["training"]["model"]]

    return Settings(
        **raw,
        algorithm_config=algo_cls(**raw.get("algorithm_config", {})),
        model_config=model_cls(**raw.get("model_config", {})),
    )
```

---

## Config Resolution Order

Highest priority first:

1. CLI flags (passed as `overrides` dict to `load_settings`)
2. YAML file values
3. Pydantic field defaults (`models.py` and subclass defaults)

---

## Invariants

1. The top-level YAML keys (`env`, `training`, `anyscale`, `algorithm_config`, `model_config`) are always present — missing sections raise a validation error
2. Unknown keys at any level raise a validation error (`extra="forbid"`)
3. `training.algorithm` must be a key in `ALGORITHM_CONFIGS` — unrecognised values raise at load time, not at training time
4. `training.model` must be a key in `MODEL_CONFIGS` — same rule
5. `settings.py` is the only place YAML is read — nothing else opens the config file directly
