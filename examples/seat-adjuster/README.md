# Seat-adjuster example


## Launch the seat-adjuster example

```bash
cd examples/seat-adjuster/src

dapr run --app-id seatadjuster --app-protocol grpc --app-port 50008 --config ../../.dapr/config.yaml --resources-path ../../.dapr/components  python3 main.py
```
