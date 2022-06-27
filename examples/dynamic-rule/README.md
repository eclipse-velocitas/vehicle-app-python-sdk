# Dynamic-rule example


## Launch the dynamic-rule example

```bash
cd examples/dynamic-rule

# with dapr enabled
dapr run --app-id speedlimitwarner --app-protocol grpc --app-port 50008 --config ../../.dapr/config.yaml --components-path ../../.dapr/components -- python3 run.py -e
```

```bash
cd examples/dynamic-rule

# without dapr enabled
python3 run.py
```

### Flags
| Flag | Description | Usage |
|---------|-------------|-------|
| -l or --limit | Pass speed limit dynamically (defaults to 130) | python3 run.py -l 120 <br/> python3 run.py --limit 120
|-e or --enable-dapr | Pass flag to enable dapr | python3 run.py -e <br/> python3 run.py --enable-dapr
