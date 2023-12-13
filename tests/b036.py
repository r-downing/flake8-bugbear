
try:
    pass
except BaseException:  # bad
    print("aaa")
    pass


try:
    pass
except BaseException as ex:  # bad
    print(ex)
    pass


try:
    pass
except ValueError:
    raise
except BaseException:  # bad
    pass


try:
    pass
except BaseException:  # ok - reraised
    print("aaa")
    raise


try:
    pass
except BaseException as ex:  # bad - raised something else
    print("aaa")
    raise KeyError from ex
