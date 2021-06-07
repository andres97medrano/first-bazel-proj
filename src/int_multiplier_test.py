import unittest
from int_multiplier import IntMultiplier

class IntMultiplierTest(unittest.TestCase):
    
    def test_int_multiplier(self):
        im = IntMultiplier(a=3, b=5)
        self.assertEquals(15, im.get_product())
