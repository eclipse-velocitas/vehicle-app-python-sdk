# Seat-adjuster example

:warning: This example is currently not executable from within the vehicle-app-pytthon-sdk's devContainer. Please use the "import example" feature of the related [vehicle-app-python-template repository](https://github.com/eclipse-velocitas/vehicle-app-python-template). Also, building the docker container for this example needs to be done after the import within the Python template's devContainer.


## Run this example from your Python app development repo

It is possible to import and run this example from your app development repository, which you already have created or could create from our [vehicle-app-python-template repository](https://github.com/eclipse-velocitas/vehicle-app-python-template).

1. Importing the example

   Use the VS Code task `Import example app from SDK` (to get there press `Ctrl+Shift+P` and select `Tasks: Run Task`) and choose `seat-adjuster` from the list.

   :warning: Make sure you have commited or stash all your possible changes within the `app` folder, because the files of that folder will be overwritten by the files of this example.

2. Running this example with Dapr middleware

   Use the VS Code tasks `Local Runtime - Up` and `Local Runtime - Run VehicleApp` to start the necessary runtime components and this app itself.

   Alternatively, the app can also be deployed in a k3d runtime - use task `K3D Runtime - Deploy VehicleApp`.


## Executing with "native" middleware (without Dapr runtime)

If you like to run this example without using Dapr as middleware, you may need to provide some environment variables to the seat-adjuster process, which define where to find the required runtime components:

| Variable name                   | Default value            | Description
|---------------------------------|--------------------------|-------------
| `SDV_MQTT_ADDRESS`              | `mqtt://localhost:1883`  | Address (and port) of the MQTT broker
| `SDV_VEHICLEDATABROKER_ADDRESS` | `grpc://localhost:55555` | Address (and port) of the KUKSA Data Broker
