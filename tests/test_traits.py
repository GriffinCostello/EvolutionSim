from src.traits import Traits, FoodTraits, FoodStage


def test_mustation_with_nonzero_variance():
    value = 10
    variance = 2
    minimum = 5
    results = []
    for _ in range(100):
        mutated_value = Traits.mutate(value, variance, minimum)
        results.append(mutated_value)
    
    assert all(minimum <= v <= value + variance for v in results)
    assert len(results) >= 3

def test_mutate_with_zero_variance_returns_value_or_minimum():
    assert Traits.mutate(10, 0, 1) == 10
    assert Traits.mutate(2, 0, 5) == 5


def test_foodtraits_stage_durations_and_nutrition():
    cfg = {
        FoodStage.SEED: {"duration": 2, "nutrition": 1},
        FoodStage.RIPENING: {"duration": 3, "nutrition": 2},
        FoodStage.RIPE: {"duration": 1, "nutrition": 5},
    }

    ft = FoodTraits(0, cfg)

    assert ft.stageDurations[FoodStage.SEED] == (0, 2)
    assert ft.stageDurations[FoodStage.RIPENING] == (2, 5)
    assert ft.stageDurations[FoodStage.RIPE] == (5, 6)

    assert ft.nutritionalValue[FoodStage.RIPE] == 5
    assert ft.totalLifespan == 6
