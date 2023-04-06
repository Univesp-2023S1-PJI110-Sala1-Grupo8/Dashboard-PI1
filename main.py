# Application entry point.

import sys
sys.path.insert(0, './model/')
import _test_model as tm

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tm.test_model()