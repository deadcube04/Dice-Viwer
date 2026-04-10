from enum import Enum


class DICE_CLASS(Enum):
    D4 = (1, 4)
    D6 = (1, 6)
    D8 = (1, 8)
    D10 = (0, 9)
    D100 = (00, 90)
    D12 = (1, 12)
    D20 = (1, 20)

    def __init__(self, min_number, max_number):
        self.max_number = max_number
        self.min_number = min_number


class Dice:
    @staticmethod
    def calculate_oposite_side(dice_type : DICE_CLASS, dice_value : int) -> int:
        match dice_type:
            case DICE_CLASS.D4:
                return None
            case DICE_CLASS.D6: # ok
                return 7 - dice_value
            case DICE_CLASS.D8: # Lookup only
                return None
            case DICE_CLASS.D10: # ok
                return 9 - dice_value 
            case DICE_CLASS.D12: # ok
                return 13 - dice_value
            case DICE_CLASS.D20: # ok
                return 21 - dice_value
            case DICE_CLASS.D100: # ok
                return 90 - dice_value
    @staticmethod
    def validate_dice_value(dice_type : DICE_CLASS, dice_value : int) -> bool:
        is_valid = dice_type.min_number <= dice_value <= dice_type.max_number
        
        if dice_type == DICE_CLASS.D100:
            is_valid = (dice_value % 10 == 0) and is_valid
        
        return is_valid


