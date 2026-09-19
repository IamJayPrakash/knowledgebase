# Low-Level Design (LLD): Scalable Multi-Floor Parking Lot System

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Parking lot ek **Object-Oriented Mall Parking** hai.
Gaadiyan alag-alag type ki hoti hain (Bike, Car, Truck). Har gaadi ke liye alag size ka spot chahiye (Compact, Large, Handicapped).
System ko pata hona chahiye ki:
- Gaadi aayi -> Ticket print karo jisme entry time ho.
- Gaadi gayi -> Total hours calculate karo, fee calculate karo, aur spot ko khali mark karo.
- SOLID Principles aur Strategy Pattern use karo taaki agar kal nayi Electric Car parking ya Hourly Fee rule badal jaye, toh pura code na rewrite karna pade!

---

## 📌 2. Core OOP Design Patterns Applied
1. **Singleton Pattern**: For `ParkingLot` central instance.
2. **Factory Pattern**: For `Vehicle` and `ParkingFeeStrategy` instantiation.
3. **Strategy Pattern**: For calculating parking charges (Flat rate vs Hourly vs Dynamic peak rate).

---

## 💻 3. Line-by-Line Commented Code Solution (Python)

```python
from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime
import uuid

# Line 7: Vehicle and Spot Type Enums
class VehicleType(Enum):
    MOTORCYCLE = 1
    CAR = 2
    TRUCK = 3

class SpotType(Enum):
    COMPACT = 1
    MEDIUM = 2
    LARGE = 3

# Line 18: Parking Spot Abstraction
class ParkingSpot:
    def __init__(self, spot_id: str, floor_id: int, spot_type: SpotType):
        self.spot_id = spot_id
        self.floor_id = floor_id
        self.spot_type = spot_type
        self.is_occupied = False
        self.vehicle = None

    def park(self, vehicle):
        self.vehicle = vehicle
        self.is_occupied = True

    def unpark(self):
        self.vehicle = None
        self.is_occupied = False

# Line 36: Strategy Pattern for Pricing
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, hours: float, vehicle_type: VehicleType) -> float:
        pass

class HourlyPricingStrategy(PricingStrategy):
    RATES = {
        VehicleType.MOTORCYCLE: 10.0,
        VehicleType.CAR: 20.0,
        VehicleType.TRUCK: 50.0
    }

    def calculate_fee(self, hours: float, vehicle_type: VehicleType) -> float:
        rate = self.RATES.get(vehicle_type, 20.0)
        return max(1.0, hours) * rate

# Line 53: Parking Ticket Entity
class Ticket:
    def __init__(self, spot: ParkingSpot, vehicle_type: VehicleType):
        self.ticket_id = str(uuid.uuid4())[:8]
        self.spot = spot
        self.vehicle_type = vehicle_type
        self.entry_time = datetime.now()

# Line 61: Central ParkingLot Coordinator (Singleton)
class ParkingLot:
    def __init__(self, pricing_strategy: PricingStrategy):
        self.spots = []
        self.pricing_strategy = pricing_strategy

    def add_spot(self, spot: ParkingSpot):
        self.spots.append(spot)

    def issue_ticket(self, vehicle_type: VehicleType) -> Ticket:
        for spot in self.spots:
            if not spot.is_occupied:
                spot.park(vehicle_type)
                return Ticket(spot, vehicle_type)
        raise Exception("Parking Lot is Full!")

    def process_exit(self, ticket: Ticket, duration_hours: float) -> float:
        ticket.spot.unpark()
        return self.pricing_strategy.calculate_fee(duration_hours, ticket.vehicle_type)
```
