from lewis import Simulation, Device, EpicsInterface


class MyDevice(Device):
    ...


class MyInterface(EpicsInterface):
    ...


if __name__ == '__main__':
    sim = Simulation(...)

    dev1 = sim.createDevice(MyDevice, MyInterface(prefix='DEV1:'))
    dev2 = sim.createDevice(MyDevice, MyInterface(prefix='DEV2:'))

    sim.speed = 1.2
    sim.cycles_per_sec = 10

    sim.enableControlServer(port=10000)

    # blocking until terminated
    sim.run()


