from __future__ import annotations

"""
Domain primitive types for the GuildQuest Mini-Adventure Environment (GMAE).

Classes
-------
    Name: generic alphanumeric string which may contain spaces
    Description: may contain punctuation
    Username   – alphanumeric player handle used to identify a Player
    QuestName  – alphanumeric label assigned to a MiniQuest.
    Coordinate – non-negative (row, col) grid position with spatial helpers.
    Qty        – non-negative integer quantity (scores, counts, capacities).
    RealmSize  – integer realm dimension constrained to the range [4, 20].
"""
from __future__ import annotations

# ─────────────────────────────────────────────────────────────────────────────
# Internal shared helpers
# ─────────────────────────────────────────────────────────────────────────────

def _check_len_between(min: int, max: int, string: str, label: str):
    """ 
    checks that string is between min and max characters inclusive
    or raises valueerror
    """
    if len(string) < min:
        raise ValueError(f"{label} has less than {min} characters")
    if len(string) > max:
        raise ValueError(f"{label} has more than {max} characters")

def _require_alphanum_or_in(value: str, label: str, charset: str) -> str:
    _ALLOWED_EXTRAS: frozenset[str] = frozenset(charset)

    stripped = value.strip()

    invalid = [ch for ch in stripped if not ch.isalnum() and ch not in _ALLOWED_EXTRAS]
    if invalid:
        raise ValueError(f"Only alphanumeric characters, spaces, commas, and periods are allowed in {label}")

    return stripped

def _require_alphanumeric_or_punctuation(value: str, label: str) -> str:
    return _require_alphanum_or_in(value, label, " ,.")

def _require_alphanumeric_or_space(value: str, label: str) -> str:
    return _require_alphanum_or_in(value, label, " ")

def _require_alphanumeric(value: str, label: str) -> str:
    """Strip whitespace, enforce non-empty, and enforce alphanumeric-only.

    Returns the stripped string on success; raises ValueError on failure.
    Used internally by both Username and QuestName.
    """
    stripped = value.strip()
    if not stripped.isalnum():
        raise ValueError(
            f"{label} must contain only alphanumeric characters "
            f"(letters and digits, no spaces or symbols), got: {stripped!r}"
        )
    return stripped


# ─────────────────────────────────────────────────────────────────────────────
# Username and QuestName
# ─────────────────────────────────────────────────────────────────────────────

class _Text:
    """
    Trimmed string containing [MIN, MAX] characters of any kind.
    """
    LABEL: str = ""
    MIN_LEN: int = 3
    MAX_LEN: int = 15
    _value: str = ""

    def __init__(self, value: str) -> None:
        self._value = value
        _check_len_between(self.MIN_LEN, self.MAX_LEN, value, self.LABEL)

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

    @property
    def value(self) -> str:
        """The validated username string (read-only)."""
        return self._value

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"Username({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, _Text):
            return self._value == other._value
        if isinstance(other, str):           # allow direct str comparison
            return self._value == other
        return NotImplemented

    def __len__(self) -> int:
        """Return the number of characters in the username."""
        return len(self._value)

class _SpaceableText(_Text):
    def __init__(self, value: str) -> None:
        value = _require_alphanum_or_in(value, self.LABEL, " ")
        super().__init__(value)

class _PunctuatedText(_Text):
    def __init__(self, value: str) -> None:
        value = _require_alphanum_or_in(value, self.LABEL, " ,.")
        super().__init__(value)

class _AlphanumText(_Text):
    def __init__(self, value: str) -> None:
        value = _require_alphanumeric(value, self.LABEL)
        super().__init__(value)

class Name(_SpaceableText):
    LABEL: str = "Name"
    MIN_LEN: int = 3
    MAX_LEN: int = 15

class Username(_AlphanumText):
    LABEL: str = "Username"
    MIN_LEN: int = 3
    MAX_LEN: int = 8
    
class QuestName(Name):
    pass

class Description(_PunctuatedText):
    LABEL: str = "Description"
    MIN_LEN: int = 0
    MAX_LEN: int = 100

# ─────────────────────────────────────────────────────────────────────────────
# Coordinate
# ─────────────────────────────────────────────────────────────────────────────

class Coordinate:
    """An immutable, non-negative (row, col) grid position.

    Attributes
    ----------
    x : int  – row index (zero-based).
    y : int  – column index (zero-based).

    Raises
    ------
    TypeError
        If ``x`` or ``y`` is not an ``int`` (booleans are explicitly rejected).
    ValueError
        If ``x`` or ``y`` is negative, or if an operation would produce a
        negative component.
    """

    def __init__(self, x: int, y: int) -> None:
        if isinstance(x, bool) or not isinstance(x, int):
            raise TypeError(
                f"Coordinate x must be an int, got {type(x).__name__}"
            )
        if isinstance(y, bool) or not isinstance(y, int):
            raise TypeError(
                f"Coordinate y must be an int, got {type(y).__name__}"
            )
        if x < 0:
            raise ValueError(f"Coordinate x must be non-negative, got {x}")
        if y < 0:
            raise ValueError(f"Coordinate y must be non-negative, got {y}")
        self._x: int = x
        self._y: int = y

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

    @property
    def x(self) -> int:
        """Row index (zero-based, read-only)."""
        return self._x

    @property
    def y(self) -> int:
        """Column index (zero-based, read-only)."""
        return self._y

    # ------------------------------------------------------------------ #
    # Core spatial operations
    # ------------------------------------------------------------------ #

    def translate(self, offset: "Coordinate") -> "Coordinate":
        """Return a new Coordinate shifted by *offset* (vector addition).

        Raises
        ------
        TypeError
            If *offset* is not a ``Coordinate``.
        """
        if not isinstance(offset, Coordinate):
            raise TypeError(
                f"translate() expects a Coordinate, got {type(offset).__name__}"
            )
        return Coordinate(self._x + offset._x, self._y + offset._y)

    def is_adjacent_to(self, other: "Coordinate") -> bool:
        """Return ``True`` if *other* is exactly one orthogonal step away.

        Two coordinates are adjacent when their Manhattan distance equals 1
        (same row, neighbouring column — or vice versa).  Diagonal positions
        are *not* considered adjacent.

        Parameters
        ----------
        other : Coordinate
            The Coordinate to compare against.
        """
        if not isinstance(other, Coordinate):
            raise TypeError(
                f"is_adjacent_to() expects a Coordinate, "
                f"got {type(other).__name__}"
            )
        dx = abs(self._x - other._x)
        dy = abs(self._y - other._y)
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

    def neighbors(self, size: int | None = None) -> list["Coordinate"]:
        """Return the up-to-four orthogonal neighbouring Coordinates.

        The four cardinal candidates (up, down, left, right) are computed;
        any that would fall outside the valid grid range are filtered out.

        Parameters
        ----------
        size : int, optional
            Side-length of the square realm.  When supplied, neighbours
            whose components meet or exceed *size* are excluded as well as
            those below zero.  When omitted, only the non-negative filter
            is applied.

        Returns
        -------
        list[Coordinate]
            Between 0 and 4 valid neighbouring Coordinates.
        """
        candidates = [
            (self._x - 1, self._y),   # up
            (self._x + 1, self._y),   # down
            (self._x,     self._y - 1),  # left
            (self._x,     self._y + 1),  # right
        ]
        result: list[Coordinate] = []
        for nx, ny in candidates:
            if nx < 0 or ny < 0:
                continue
            if size is not None and (nx >= size or ny >= size):
                continue
            result.append(Coordinate(nx, ny))
        return result

    # ------------------------------------------------------------------ #
    # Bounds helpers
    # ------------------------------------------------------------------ #

    def is_within_bounds(self, size: int) -> bool:
        """Return ``True`` if this position is inside a square realm of *size*.

        A coordinate is in-bounds when both components satisfy
        ``0 <= component < size``.  Mirrors the logic of the existing
        ``Realm.in_bounds`` method so that callers can validate a
        ``Coordinate`` without a ``Realm`` reference.

        Parameters
        ----------
        size : int
            The side-length of the square grid (must be a positive int).
        """
        if isinstance(size, bool) or not isinstance(size, int) or size <= 0:
            raise ValueError(
                f"size must be a positive int, got {size!r}"
            )
        return self._x < size and self._y < size

    # ------------------------------------------------------------------ #
    # Operator overloads
    # ------------------------------------------------------------------ #

    def __add__(self, other: "Coordinate") -> "Coordinate":
        """Alias for :meth:`translate`  →  ``pos + offset``."""
        return self.translate(other)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Coordinate):
            return self._x == other._x and self._y == other._y
        return NotImplemented

    def __repr__(self) -> str:
        return f"Coordinate({self._x}, {self._y})"

    def __str__(self) -> str:
        return f"({self._x}, {self._y})"


# ─────────────────────────────────────────────────────────────────────────────
# Qty
# ─────────────────────────────────────────────────────────────────────────────

class Qty:
    """A non-negative integer quantity.

    Arithmetic
    ----------
    - Addition always produces a new ``Qty``.
    - Subtraction saturates at zero by default (no underflow exception);
      pass ``strict=True`` to :meth:`decrement` if you need the exception.
    - Multiplication produces a new ``Qty``.
    - All comparison operators work against both ``Qty`` and plain ``int``.

    Raises
    ------
    TypeError
        If *value* is not an ``int`` (booleans are explicitly rejected).
    ValueError
        If *value* is negative.
    """

    def __init__(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(
                f"Qty value must be an int, got {type(value).__name__}"
            )
        if value < 0:
            raise ValueError(f"Qty cannot be negative, got {value}")
        self._value: int = value

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #

    @property
    def value(self) -> int:
        """The underlying non-negative integer (read-only)."""
        return self._value

    # ------------------------------------------------------------------ #
    # Internal coercion helper
    # ------------------------------------------------------------------ #

    def _coerce(self, other: object) -> int:
        """Return the int value of *other*, or raise TypeError."""
        if isinstance(other, Qty):
            return other._value
        if isinstance(other, int) and other >= 0:
            return other
        raise TypeError(
            f"Qty arithmetic requires a Qty or non-negative int, "
            f"got {type(other).__name__}"
        )

    # ------------------------------------------------------------------ #
    # Arithmetic operators
    # ------------------------------------------------------------------ #

    def __add__(self, other: object) -> "Qty":
        return Qty(self._value + self._coerce(other))

    def __radd__(self, other: object) -> "Qty":
        return Qty(self._coerce(other) + self._value)

    def __sub__(self, other: object) -> "Qty":
        """Saturating subtraction — result is clamped to 0, never negative."""
        return Qty(max(0, self._value - self._coerce(other)))

    def __rsub__(self, other: object) -> "Qty":
        return Qty(max(0, self._coerce(other) - self._value))

    def __mul__(self, other: object) -> "Qty":
        return Qty(self._value * self._coerce(other))

    def __rmul__(self, other: object) -> "Qty":
        return Qty(self._coerce(other) * self._value)

    # ------------------------------------------------------------------ #
    # Comparison operators
    # ------------------------------------------------------------------ #

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Qty):
            return self._value == other._value
        if isinstance(other, int):
            return self._value == other
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Qty):
            return self._value < other._value
        if isinstance(other, int):
            return self._value < other
        return NotImplemented

    def __le__(self, other: object) -> bool:
        if isinstance(other, Qty):
            return self._value <= other._value
        if not isinstance(other, bool) and isinstance(other, int):
            return self._value <= other
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Qty):
            return self._value > other._value
        if not isinstance(other, bool) and isinstance(other, int):
            return self._value > other
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        if isinstance(other, Qty):
            return self._value >= other._value
        if not isinstance(other, bool) and isinstance(other, int):
            return self._value >= other
        return NotImplemented

    # ------------------------------------------------------------------ #
    # Conversion / display
    # ------------------------------------------------------------------ #

    def __int__(self) -> int:
        return self._value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"Qty({self._value})"

# ─────────────────────────────────────────────────────────────────────────────
# RealmSize
# ─────────────────────────────────────────────────────────────────────────────

class RealmSize:
    """A validated realm grid dimension constrained to the range [MIN, MAX].

    ---------------
    MIN : int = 4
    MAX : int = 20

    Raises
    ------
    TypeError
        If *value* is not an ``int``.
    ValueError
        If *value* is outside [MIN, MAX].
    """

    MIN: int = 4
    MAX: int = 20

    def __init__(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(
                f"RealmSize value must be an int, got {type(value).__name__}"
            )
        if not (self.MIN <= value <= self.MAX):
            raise ValueError(
                f"RealmSize must be between {self.MIN} and {self.MAX} "
                f"inclusive, got {value}"
            )
        self._value: int = value

    @property
    def value(self) -> int:
        """The validated realm dimension (read-only)."""
        return self._value

    # ------------------------------------------------------------------ #
    # Spatial helpers
    # ------------------------------------------------------------------ #

    def in_bounds(self, coord: Coordinate) -> bool:
        """Return ``True`` if *coord* is a valid position within this realm.

        A Coordinate is in-bounds when both components satisfy
        ``0 <= component < size``.  Provides a typed alternative to the
        existing ``Realm.in_bounds(x, y)`` raw-int check.

        Parameters
        ----------
        coord : Coordinate
            The grid position to validate.
        """
        if not isinstance(coord, Coordinate):
            raise TypeError(
                f"in_bounds() expects a Coordinate, got {type(coord).__name__}"
            )
        return coord.x < self._value and coord.y < self._value

    def in_bounds_xy(self, x: int, y: int) -> bool:
        """Return ``True`` if the raw ``(x, y)`` pair lies within this realm.

        Backwards-compatible variant that accepts plain ``int`` arguments —
        mirrors the signature of the existing ``Realm.in_bounds`` method so
        callers can be migrated incrementally.
        """
        return 0 <= x < self._value and 0 <= y < self._value

    # ------------------------------------------------------------------ #
    # Class-level helpers
    # ------------------------------------------------------------------ #

    @classmethod
    def is_valid(cls, value: int) -> bool:
        """Return ``True`` if *value* is a valid realm size, without raising.

        Safe to call in input-validation loops such as
        ``CreateQuest._get_realm_size()``.
        """
        if isinstance(value, bool) or not isinstance(value, int):
            return False
        return cls.MIN <= value <= cls.MAX

    # ------------------------------------------------------------------ #
    # Comparison operators
    # ------------------------------------------------------------------ #

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RealmSize):
            return self._value == other._value
        if not isinstance(other, bool) and isinstance(other, int):
            return self._value == other
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, RealmSize):
            return self._value < other._value
        if not isinstance(other, bool) and isinstance(other, int):
            return self._value < other
        return NotImplemented

    def __le__(self, other: object) -> bool:
        if isinstance(other, RealmSize):
            return self._value <= other._value
        if not isinstance(other, bool) and isinstance(other, int):
            return self._value <= other
        return NotImplemented

    def __gt__(self, other: object) -> bool:
        if isinstance(other, RealmSize):
            return self._value > other._value
        if not isinstance(other, bool) and isinstance(other, int):
            return self._value > other
        return NotImplemented

    def __ge__(self, other: object) -> bool:
        if isinstance(other, RealmSize):
            return self._value >= other._value
        if not isinstance(other, bool) and isinstance(other, int):
            return self._value >= other
        return NotImplemented
   
    # ------------------------------------------------------------------ #
    # Conversion / display
    # ------------------------------------------------------------------ #

    def __int__(self) -> int:
        return self._value

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"RealmSize({self._value})"
