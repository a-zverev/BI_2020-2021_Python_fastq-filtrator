import sys


KEEP_FILTERED = False
MIN_LEN = 1
OUTPUT_BASENAME = ''
GC_BOUND = []

# is it help request?
if len(sys.argv) == 1 or sys.argv[1] == '--help':
    print("this is help")
    exit()

# parse mandatory arg. Actually os.path is better, but we can`t use it :/
file = sys.argv[-1]
try:
    f = open(file, 'r')
    f.read(16)
    f.close()
except IOError:
    raise ValueError(f"Can't open file: {file}")

# parse optional args
list = sys.argv[1: -1]

while list:
    arg = list.pop(0)

    if arg == "--min_length":
        # int more than 0
        if list and not list[0].startswith("--"):
            value = list.pop(0)
            if value.isdigit() and int(value) > 0:
                MIN_LEN = value
            else:
                raise ValueError(f"Wrong value in --min_length: {value}")
        else:
            raise ValueError(f"No argument with --min_length")

    elif arg == "--keep_filtered":
        # flag
        KEEP_FILTERED = True

    if arg == "--gc_bounds":
        # int more 0, upper >= lower
        if list and not list[0].startswith("--"):
            GC_BOUND.append(list.pop(0))
        elif list and not list[0].startswith("--"):
            GC_BOUND.append(list.pop(0))
        for value in GC_BOUND:
            if not value.isdigit() or int(value) < 0:
                raise ValueError(f"Wrong value {value}")
        if len(GC_BOUND) == 2 and GC_BOUND[0] > GC_BOUND[1]:
            raise ValueError(f"Wrong --gc_bounds values: min is greater, than max")
        else:
            raise ValueError(f"No argument with --gc_bounds")

    if arg == "--output_base_name":
        # name
        if list and not list[0].startswith("--"):
            OUTPUT_BASENAME = list.pop(0)
        else:
            raise ValueError(f"No argument with --output_base_name")

    else:
        raise ValueError(f"Unknown argument: {arg}")


print(KEEP_FILTERED, MIN_LEN, OUTPUT_BASENAME, GC_BOUND)