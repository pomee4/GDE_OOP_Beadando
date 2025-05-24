# Legitárság osztály
class LegiTarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []

    def add_jarat(self, jarat):
        """Hozzáad egy járatot a légitársasághoz."""
        self.jaratok.append(jarat)

    def get_jaratok(self):
        """Visszaadja a légitársaság összes járatát."""
        return self.jaratok
