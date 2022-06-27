# Eclipse Velocitas Vehicle Dog Mode Sample App

## Use Case

The *Dog Mode* app is a climate control app that allows drivers to leave their vehicles while keeping the air conditioning system of the vehicle active for their pets.
The application consists of  the following key features:

* Request the vehicle's Heating, Ventilation, and Air Conditioning (HVAC) service to turn the Air Conditioning (AC) ON/OFF
* The driver can adjust the temperature for a specific degree
* The app observe the current temperature and the battery's state of charge and react accordingly
* The driver/owner will be notified whenever the state of the charge drops below a certain value

## Launch the HVAC Service
In order to launch the Heating, Ventilation, and Air Conditioning (HVAC) Service please use Visual Studio Code Tasks via:
- Window: `CTRL+SHIFT+P -> Tasks: Run Tasks -> run-hvacservice (Runtime)`
- Mac: `CMD+SHIFT+P -> Tasks: Run Tasks -> run-hvacservice (Runtime)`

## Launch the Sample App
* Navigate to the examples directory
```bash
    cd examples/
```

* Run the dog mode sample app

Please use the script below to launch the dog mode sample app.

```bash
    dapr run \
    --app-id dogmode \
    --app-protocol grpc \
    --app-port 50008 \
    --config ../.dapr/config.yaml  \
    --components-path ../.dapr/components python3 dog-mode/run.py
```

Alternative, run the Visual Studio Code task `"DogMode (Dapr run)"` or use the script [run-app.sh](./../run-app.sh) as below:
```bash
./run-app.sh -a dog-mode
```

## Use of [AsyncIOScheduler](https://apscheduler.readthedocs.io/en/3.x/modules/schedulers/asyncio.html)

If you plan to use the *AsyncIOScheduler* in your application in order to execute any asynchronous periodic calls in the [AsyncIO](https://docs.python.org/3/library/asyncio.html) event loop, this app provides an example of one way how that can be realized.

In this sample app, the *AsyncIOScheduler* is used to periodically display the current ambient temperature and battery state of charge every 30 second via MQTT. The code snippet shows how this is implemented.

```python
    # This is the on_start() method of the VehicleApp
    async def on_start(self):
        logger.info("VehicleApp Started ...")
        try:
            await self.display_values()

            # Create an instance of the AsyncIOScheduler
            self.scheduler = AsyncIOScheduler()

            # Add the Job that needs to be scheduled periodically with a reference to the target function.
            self.scheduler.add_job(
                self.display_values, "interval", seconds=TEMP_REPORT_TIMEOUT
            )

            # Start the AsyncIOScheduler
            self.scheduler.start()
        except Exception as ex:
            logger.error(ex)

    # This is the target function of the AsyncIOScheduler
    async def display_values(self):
        logger.info("Publish Current Temperature and StateOfCharge")
        # Add your code here ...

```

## Display the Current Temperature and State Of Charge

In order to receive the current ambient temperature and battery state of charge, you need to subscribe for the MQTT topic below:
```
    dogmode/display
```
If the VehileApp runtime services together with the HVAC service are running, you shall be able to see the result in the *VSMQTT* cliant as below:
```
    {"Temperature": 24.0, "StateOfCharge": 91.0}
```
