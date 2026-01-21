from src.traits import Traits, FoodTraits, FoodStage

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
