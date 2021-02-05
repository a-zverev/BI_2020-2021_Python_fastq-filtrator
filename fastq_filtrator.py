import sys

KEEP_FILTERED = False
MIN_LEN = 1
OUTPUT_BASENAME = ''
GC_BOUND = []

# is it help request?
if len(sys.argv) == 1 or sys.argv[1] == '--help':
    print("This is simple fastq filtrator by GC-content and length.")
    print("Usage: fastq_filtrator.py [options] FILE")
    print("mandatory argument:")
    print("FILE - name of fastq-file")
    print("optional arguments:")
    print("--min_length N  - minimal length of read to survive, int value. If not provided, "
          "all reads will pass length filter")
    print("--keep_filtered  - keep filtered reads in separate file, flag")
    print("--gc_bounds N [N]  - range for filtration. if one value is provided, no upper bound will be set. "
          "If not provided, all reads will pass GC-content filter")
    print("--output_base_name NAME  - prefix for output file. If not specified, name of FILE will be used "
          "as a output name")
    exit()

# parse mandatory arg. Actually os.path is better, but we can`t use it :/
file = sys.argv[-1]
if file.startswith("--"):
    raise ValueError("No file")
try:
    f = open(file, 'r')
    f.read(16)
    f.close()
except IOError:
    raise ValueError(f"Can't open file: {file}")
OUTPUT_BASENAME = ".".join(file.split(".")[:-1])

# parse optional args
list = sys.argv[1: -1]
# print(list)

while list:
    arg = list.pop(0).strip()
#     print(arg)
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

    elif arg == "--gc_bounds":
        # ints more 0, upper >= lower
        if list and not list[0].startswith("--"):
            GC_BOUND.append(list.pop(0))
            if list and not list[0].startswith("--"):
                GC_BOUND.append(list.pop(0))
        else:
            raise ValueError(f"No argument with --gc_bounds")

        for value in GC_BOUND:
            if not value.isdigit() or int(value) < 0:
                raise ValueError(f"Wrong value {value}")
        if len(GC_BOUND) == 2 and GC_BOUND[0] > GC_BOUND[1]:
            raise ValueError(f"Wrong --gc_bounds values: min is greater, than max")

    elif arg == "--output_base_name":
        # name
        if list and not list[0].startswith("--"):
            OUTPUT_BASENAME = list.pop(0)
        else:
            raise ValueError(f"No argument with --output_base_name")

    else:
        raise ValueError(f"Unknown argument: {arg}")


print(f'keep filtered is {KEEP_FILTERED}, '
      f'min len is {MIN_LEN}, '
      f'basename is {OUTPUT_BASENAME}, '
      f'gc range is  {GC_BOUND}')


# from https://www.biostars.org/p/317524/
def process(lines_in=None):
    ks = ['name', 'sequence', 'optional', 'quality']
    return {k: v for k, v in zip(ks, lines_in)}


n = 4
res = []
with open(file, 'r') as fh:
    lines = []
    for line in fh:
        lines.append(line.rstrip())
        if len(lines) == n:
            record = process(lines)
            res.append(record)
            lines = []

keep = []

if MIN_LEN:
    new_res = []
    for seq in res:
        if len(seq['sequence']) < int(MIN_LEN):
            if KEEP_FILTERED:
                keep.append(seq)
            # print("len keep ", seq)
        else:
            # print("len pass ", seq)
            new_res.append(seq)
    res = new_res

if GC_BOUND:
    new_res = []
    for seq in res:
        seq_len = len(seq['sequence'])
        gc_sum = seq['sequence'].count('C') + seq['sequence'].count('G')
        gc_per = (gc_sum / seq_len) * 100

        if len(GC_BOUND) == 1:
            if gc_per > float(GC_BOUND[0]):
                new_res.append(seq)
            else:
                if KEEP_FILTERED:
                    keep.append(seq)
        else:
            if float(GC_BOUND[0]) < gc_per < float(GC_BOUND[1]):
                new_res.append(seq)
                print("gc pass ", seq)
            else:
                if KEEP_FILTERED:
                    # print("gc keep ", seq, ' ', float(GC_BOUND[0]), ' < ', gc_per, ' < ', float(GC_BOUND[1]))
                    keep.append(seq)
    res = new_res

# print(res)

if KEEP_FILTERED:
    filename_passed = "%s__passed.fastq" % OUTPUT_BASENAME
    filename_keep = "%s__failed.fastq" % OUTPUT_BASENAME
    with open(filename_passed, 'w', encoding='utf-8') as f:
        for i in res:
            f.write(i['name'] + '\n')
            f.write(i['sequence'] + '\n')
            f.write(i['optional'] + '\n')
            f.write(i['quality'] + '\n')
    with open(filename_keep, 'w', encoding='utf-8') as f:
        for i in keep:
            f.write(i['name'] + '\n')
            f.write(i['sequence'] + '\n')
            f.write(i['optional'] + '\n')
            f.write(i['quality'] + '\n')
else:
    filename = "%s.fastq" % OUTPUT_BASENAME
    with open(filename, 'w', encoding='utf-8') as f:
        for i in res:
            f.write(i['name'] + '\n')
            f.write(i['sequence'] + '\n')
            f.write(i['optional'] + '\n')
            f.write(i['quality'] + '\n')
