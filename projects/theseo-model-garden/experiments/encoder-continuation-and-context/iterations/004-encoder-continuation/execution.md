# Encoder-continuation execution

Source `2423714` compared the existing encoder at 48- and 192-geometry probe exposure,
three freshly initialized same-architecture encoders pretrained on 192 geometries for
2,048 updates, and the refined supervised reference. All arms shared fresh selection
and assessment sets. Probe capacity and thresholds were selected on selection only;
the encoder checkpoint was the final pretraining checkpoint. The registered paired
assessment used three seeds and a geometry-cluster bootstrap.
