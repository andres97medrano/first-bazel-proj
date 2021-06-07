from int_multiplier import IntMultiplier


def hello_world():
    print("Hello World!")
    im = IntMultiplier(3, 4)
    print(im.get_product())

if __name__ == "__main__":
    hello_world()
