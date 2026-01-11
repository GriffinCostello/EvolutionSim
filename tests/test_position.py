from src.position import Position

def test_distanceTo():
    posit1 = Position(0, 0)
    posit2 = Position(3, 4)
    assert posit1.distanceTo(posit2) == 5.0

def test_distanceSquaredTo():
    posit1 = Position(0, 0)
    posit2 = Position(3, 4)
    assert posit1.distanceSquaredTo(posit2) == 25

def test_asTuple():
    posit1 = Position(5.7, 8.3)
    posit2 = Position(-2.4, 3.9)
    assert posit1.asTuple() == (5, 8)
    assert posit2.asTuple() == (-2, 3)