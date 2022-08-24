# Dynamic-rule example


## Launch the dynamic-rule example

```bash
cd examples/dynamic-rule/src

# with dapr enabled
dapr run --app-id speedlimitwarner --app-protocol grpc --app-port 50008 --config ../../.dapr/config.yaml --components-path ../../.dapr/components -- python3 main.py -e
```

```bash
cd examples/dynamic-rule/src

# without dapr enabled
python3 main.py
```

### Flags
| Flag | Description | Usage |
|---------|-------------|-------|
| -l or --limit | Pass speed limit dynamically (defaults to 130) | python3 main.py -l 120 <br/> python3 main.py --limit 120
|-e or --enable-dapr | Pass flag to enable dapr | python3 main.py -e <br/> python3 main.py --enable-dapr
