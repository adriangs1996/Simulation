from seachannel import SeaChannel, LargeShip, SmallShip, MediumShip


class MultiShipsSeaChannel(SeaChannel):
    def __init__(self, hatches, func=None, debug=False):
        super().__init__(hatches, func, debug)

    def get_ships(self):
        timeS = timeM = timeL = 0

        # Generar todos los barcos pequeños, grandes y medianos
        # entre las 8:00am y 11:00am
        while timeL < 180 or timeM < 180 or timeS < 180:
            if timeL < 180:
                # Generar un nuevo barco grande
                l = LargeShip(45, 3)
                timeL = l.arrive(timeL, self.debug)
                self.ships_queue.append(l)
            if timeM < 180:
                # Generar un nuevo barco mediano
                m = MediumShip(15, 3)
                timeM = m.arrive(timeM, self.debug)
                self.ships_queue.append(m)
            if timeS < 180:
                s = SmallShip(5, 2)
                timeS = s.arrive(timeS, self.debug)
                self.ships_queue.append(s)

        # Generar los barcos entre las 11:00am y las 5:00pm
        while timeL < 540 or timeM < 540 or timeS < 540:
            if timeL < 540:
                # GEnerar un nuevo barco grande
                l = LargeShip(35, 7)
                timeL = l.arrive(timeL, self.debug)
                self.ships_queue.append(l)
            if timeM < 540:
                # Generar un nuevo barco mediano
                m = MediumShip(10, 5)
                timeM = m.arrive(timeM, self.debug)
                self.ships_queue.append(m)
            if timeS < 540:
                s = SmallShip(3, 1)
                timeS = s.arrive(timeS, self.debug)
                self.ships_queue.append(s)

        # Generar los barcos entre las 5:00pm y las 8:00pm
        while timeL < 720 or timeM < 720 or timeS < 720:
            if timeL < 720:
                # GEnerar un nuevo barco grande
                l = LargeShip(60, 9)
                timeL = l.arrive(timeL, self.debug)
                self.ships_queue.append(l)
            if timeM < 720:
                # Generar un nuevo barco mediano
                m = MediumShip(20, 5)
                timeM = m.arrive(timeM, self.debug)
                self.ships_queue.append(m)
            if timeS < 720:
                s = SmallShip(10, 2)
                timeS = s.arrive(timeS, self.debug)
                self.ships_queue.append(s)

        self.ships_queue.sort()
