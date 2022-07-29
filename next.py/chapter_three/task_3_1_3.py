
def first_error():
    print(iter([]).__next__())


def second_error():
    print(5 / 0)


def third_error():
    assert 1 != 1


def fourth_error():
    import request


def fifth_error():
    sample_dict = {1: "one"}
    print(sample_dict["make me throw an error"])


def sixth_error():
    num = 1
    # num++
    # uncomment above me


def seventh_error():
    if True:
       #  print("yes")
        # uncomment above me
        pass


def eigth_error():
    print(3 + "4")
