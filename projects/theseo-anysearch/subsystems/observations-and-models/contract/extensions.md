# Observation and model extension points

Optional representation packages may supply compatible encoders, checkpoints,
normalization metadata, and certification records without changing the base
observation or model interface. Extensions must declare compatibility, activation,
loading behavior, and the behavior of the host when the extension is absent.

## Concrete extensions

- [Model Garden](../extensions/model-garden/README.md)
