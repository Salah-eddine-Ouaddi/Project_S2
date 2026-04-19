from pathlib import Path
from src.core.logic import ParkingLogic
from src.app import ParkingApp


BASE    = Path(__file__).resolve().parent
DONNEES = BASE / "data"  / "parking.json"
OUTPUT  = BASE / "output"

if __name__ == "__main__":
    logic = ParkingLogic(DONNEES, OUTPUT)


    app = ParkingApp(logic)
    app.mainloop()