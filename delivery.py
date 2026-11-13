"""HW1: a Bangkok food-delivery order. Practises Sessions 1-3: aliasing and defaults, comprehensions,
classes with a guarded property, __repr__ and __eq__, inheritance with super(), composition and duck typing."""


class MenuItem:
    """A dish on a restaurant's menu. The price is a whole number of baht."""

    def __init__(self, name: str, price: int):
        """Store the name and the price. The price goes through the setter, so it is checked."""
        self.name = name
        self.price = price

    @property
    def price(self) -> int:
        """Provided: the price in baht."""
        return self._price

    @price.setter
    def price(self, value: int) -> None:
        """Set the price. Raise ValueError if it is 0 or less, and keep the old price."""
        if value <= 0:
            raise ValueError
        else:
            self._price = value

    def __repr__(self) -> str:
        """Return the developer view, for example MenuItem('Pad Thai', 60)."""
        return f"MenuItem({self.name!r}, {self._price!r})"

    def __eq__(self, other: object) -> bool:
        """Two menu items are equal when their names and prices are equal."""
        return self.name == other.name and self._price == other._price

    def cost(self, quantity: int) -> int:
        """Provided: what quantity of this dish costs, in baht."""
        return self.price * quantity

class PromoItem(MenuItem):
    """A dish on a "buy 2, get 1 free" promotion: every third one is free."""
    def __init__(self, name: str, price: int):
        super().__init__(name, price)

    def cost(self, quantity: int) -> int:
        """Return what quantity costs when every third one is free."""
        return (quantity - (quantity//3)) * self._price

class Order:
    """One customer's delivery order: a list of (menu item, quantity) lines."""

    delivery_fee = 30  # Provided: baht added to every order with food in it
    free_delivery_from = 300  # Provided: food worth this much or more is delivered free

    def __init__(self, customer: str, lines: list[tuple[MenuItem, int]] | None = None):
        """Store the customer and a new list of lines. Never share a list with the caller or another order."""
        self.customer = customer
        self.lines = [] if lines is None else lines.copy()

    def add(self, item: MenuItem, quantity: int = 1) -> None:
        """Add one line. Raise ValueError if quantity is less than 1."""
        if quantity < 1:
            raise ValueError
        self.lines.append((item, quantity))

    def total(self) -> int:
        """Return the food cost plus the delivery fee; free delivery from free_delivery_from; 0 if empty."""
        if self.lines == []:
            return 0
        _total = 0
        for item, quantity in self.lines:
            _total += item.cost(quantity)
        if _total > self.free_delivery_from:
            return _total
        else:
            return _total + self.delivery_fee

    def summary(self) -> list[str]:
        """Return one text line per order line, for example "2 x Pad Thai"."""
        _summary = []
        _item = {}
        for item, quantity in self.lines:
            if item.name in _item.keys():
                _item[item.name] += quantity
            else:
                _item[item.name] = quantity
        for item, quantity in _item.items():
            _summary.append(f"{quantity} x {item}")
        return _summary

def cheapest(options: list) -> object | None:
    """Return the option with the smallest total(). First one wins a tie; None for an empty list.

    An option can be anything with a total() method, not only an Order.
    """
    _min = None
    if options == []:
        return None
    for option in options:
        if _min == None or _min.total() > option.total():
            _min = option
    return option
