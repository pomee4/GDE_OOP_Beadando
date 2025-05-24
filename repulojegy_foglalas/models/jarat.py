from abc import ABC, abstractmethod

class Jarat(ABC):
    """Absztrakt alaposztály a járatokhoz."""
    def __init__(self, jaratszam, celallomas, jegyar):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = jegyar

    @abstractmethod
    def get_info(self):
        """Visszaadja a járat szöveges leírását."""
        pass

class BelfoldiJarat(Jarat):
    """Belföldi járatot reprezentáló osztály."""
    def get_info(self):
        return f"[Belföldi] {self.jaratszam} -> {self.celallomas}, Ár: {self.jegyar} Ft"

class NemzetkoziJarat(Jarat):
    """Nemzetközi járatot reprezentáló osztály."""
    def get_info(self):
        return f"[Nemzetközi] {self.jaratszam} -> {self.celallomas}, Ár: {self.jegyar} Ft"
