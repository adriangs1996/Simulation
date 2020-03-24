from numpy.random import random, exponential, normal
from math import sqrt

SMALLSIZE = 1
MEDIUMSIZE = 2
LARGESIZE = 4


class Ship:
    def __init__(self, mean, variance):
        self.mean = mean
        self.var = variance
        self.size = 0
        self.arrival = -1

    def __lt__(self, other):
        assert hasattr(other, "arrival")
        assert other.arrival > -1 and self.arrival > -1
        return self.arrival < other.arrival

    def arrive(self, time=0):
        t = abs(normal(self.mean, sqrt(self.var)))
        self.arrival = t + time
        return t


class SmallShip(Ship):
    def __init__(self, mean, var):
        super().__init__(mean, var)
        self.size = SMALLSIZE


class MediumShip(Ship):
    def __init__(self, mean, var):
        super().__init__(mean, var)
        self.size = MEDIUMSIZE


class LargeShip(Ship):
    def __init__(self, mean, var):
        super().__init__(mean, var)
        self.size = LARGESIZE


class Hatch:
    UP = 1
    DOWN = 2
    OPEN = 1
    CLOSED = 2

    def __init__(self, next_hatch=None, initial_State=1):
        # Cada dique se conecta a la siguiente, excepto el
        # ultimo que es el unico que puede despachar un barco.
        self.next_hatch = next_hatch

        # Estado en el que se encuentra la exclusa
        # (arriba o abajo).
        self.state = initial_State

        # Establecer el estado de las compuertas en dependencia
        # del estado inicial del dique
        self.up_door = Hatch.CLOSED if initial_State == Hatch.DOWN else Hatch.OPEN
        self.inf_door = Hatch.OPEN if initial_State == Hatch.DOWN else Hatch.CLOSED

        # Capacidad de la exclusa (dos filas con capacidad
        # para 3 barcos medianos)
        self.allotment = [MEDIUMSIZE * 3, MEDIUMSIZE * 3]

        # lambda del tiempo de apertura de las compuertas
        self.l_door = 1 / 4

        # lambda del tiempo que demora un barco en entrar
        self.l_ship = 1 / 2

        # lambda del tiempo de la fase de transporte
        self.l_transport = 1 / 7

        # lambda del tiempo de salida de cada barco
        self.l_departure = 1 / 1.5

        # barcos en el dique actual
        self.ships = []

    def change_state(self):
        if self.state == Hatch.UP:
            self.state = Hatch.DOWN
            self.up_door = Hatch.CLOSED
            self.inf_door = Hatch.OPEN
        elif self.state == Hatch.DOWN:
            self.state = Hatch.UP
            self.up_door = Hatch.OPEN
            self.inf_door = Hatch.CLOSED

    def last(self):
        return self.next_hatch is None

    def __iter__(self):
        hatch = self
        while not hatch.last():
            yield hatch
            hatch = hatch.next_hatch
        yield hatch

    def _put_ships(self, ships):
        for ship in ships:
            if ship.size <= self.allotment[0]:
                self.allotment[0] -= ship.size
                ship.queue = 0
                self.ships.append(ship)
            elif ship.size <= self.allotment[1]:
                self.allotment[1] -= ship.size
                ship.queue = 1
                self.ships.append(ship)

    def _remove_ships(self):
        self.allotment = [3 * MEDIUMSIZE, 3 * MEDIUMSIZE]
        s = [x for x in self.ships]
        self.ships = []
        return s

    # ---------------- Ciclo de subida --------------------

    # Definir la fase de entrada
    def up_entry(self, ships):
        t = 0

        if self.inf_door == Hatch.CLOSED:
            # abrir la puerta inferior
            t += exponential(self.l_door)
            self.inf_door = Hatch.OPEN

        # permitir la entrada de los barcos y
        # calcular el tiempo que se demoran en entrar
        self._put_ships(ships)
        # for s in self.ships:
        #   t += exponential(1 / self.l_ship)
        t += sum(exponential(self.l_ship, len(self.ships)))

        return t

    # definir la fase de transporte
    def up_transport(self):
        t = 0

        # cerrar la compuerta inferior y abrir la superior
        if self.inf_door == Hatch.OPEN:
            self.inf_door = Hatch.CLOSED
            t += exponential(self.l_door)

        if self.up_door == Hatch.CLOSED:
            self.up_door = Hatch.OPEN
            t += exponential(self.l_door)

        # llenar el dique
        t += exponential(self.l_transport)
        return t

    # definir la fase de salida
    def up_departure(self):
        # sacar los barcos del dique
        ships = self._remove_ships()
        t = sum(exponential(self.l_departure, len(ships)))
        for s in ships:
            s.departure = t

        # cerrar la puerta superior
        if self.up_door == Hatch.OPEN:
            self.up_door = Hatch.CLOSED
            t += exponential(self.l_door)

        return t, ships

    # ---------------  Ciclo de Bajada -----------------

    # definir la fase de entrada
    def down_entry(self, ships):
        t = 0

        # abrir la puerta superior
        if self.up_door == Hatch.CLOSED:
            t += exponential(self.l_door)
            self.up_door = Hatch.OPEN

        # dejar entrar los barcos
        self._put_ships(ships)
        t += sum(exponential(self.l_ship, len(self.ships)))

        return t

    # definir la fase de transporte


class HatchSystem:
    def __init__(self, hatches):
        # Construir la cadena de diques
        initial = Hatch(initial_State=hatches[-1])
        for i in range(len(hatches) - 1, -1, -1):
            initial = Hatch(next_hatch=initial, initial_State=hatches[i])


class SeaChannel:
    def __init__(self, hatches, func=None):
        self.hatches = HatchSystem(hatches)
        # Generar llegadas de barcos durante el dia.
        # El canal funciona en 3 horarios, y en cada horario, hay diferencia
        # en los parametros de la distribucion con la que llegan barcos.
        self.ships_queue = []

        # Simular la llegada entre las 8am y las 11am
        # (el tiempo entre arribos se da en minutos).
        # supongamos que cada barco puede ser de algun tipo con
        # la misma probabilidad
        time = 0
        while (time < 180):  # 180 min = 3h
            ship_rand = random()
            ship = None
            if 0 <= ship_rand <= 1 / 3:
                ship = SmallShip(5, 2)
            elif 1 / 3 < ship_rand <= 2 / 3:
                ship = MediumShip(15, 3)
            elif 2 / 3 < ship_rand <= 1:
                ship = LargeShip(45, 3)
            nt = ship.arrive()
            time = max(nt, time)
            self.ships_queue.append(ship)

        # Simular la llegada entre las 11am y las 5pm
        # Notar que 6h = 360min, eso quiere decir que estamos
        # contando en un tiempo entre 180 y 360 minutos
        while (time < 540):
            ship = None
            ship_rand = random()
            if 0 <= ship_rand <= 1 / 3:
                ship = SmallShip(5, 2)
            elif 1 / 3 < ship_rand <= 2 / 3:
                ship = MediumShip(15, 3)
            elif 2 / 3 < ship_rand <= 1:
                ship = LargeShip(45, 3)
            nt = ship.arrive(180)
            time = max(nt, time)
            self.ships_queue.append(ship)

        # Simular la llegada entre las 5pm y las 5pm y las 8pm
        # Misma idea, 180 + 540 = 720
        while (time < 720):
            ship = None
            ship_rand = random()
            if 0 <= ship_rand <= 1 / 3:
                ship = SmallShip(5, 2)
            elif 1 / 3 < ship_rand <= 2 / 3:
                ship = MediumShip(15, 3)
            elif 2 / 3 < ship_rand <= 1:
                ship = LargeShip(45, 3)
            nt = ship.arrive(540)
            time = max(nt, time)
            self.ships_queue.append(ship)

        # ordenar la cola por tiempos de arribo.
        self.ships_queue.sort()
