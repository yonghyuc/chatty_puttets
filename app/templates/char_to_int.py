ALPHABET_NUM = (ord('Z') - ord('A') + 1)

def run_integer(input_val):
    input_val = input_val.split()

    result = []
    for i in input_val:
        result.append(chr(ord('A') + (int(i) % ALPHABET_NUM)))
    print ("---------------------------------------------")
    print ("\t\t", ", ".join(result))


def run_string(input_val):
    input_val = input_val.upper()

    result = []
    for c in input_val:
        result.append(str(ord(c) - ord('A')))
    print ("---------------------------------------------")
    print (input_val)
    print ("\t\t", ", ".join(result))
    print ("\t\t", "(" + ", ".join([str(int(r)+1) for r in result]) + ")")


def run():
    while True:
        input_type = input('Enter Input type (0: integer, 1, string): ')

        if input_type == "0":
            input_val = input('Enter Integers: ')
            run_integer(input_val)
        elif input_type == "1":
            input_val = input('Enter Characters: ')
            for s in input_val.split():
                run_string(s)


if __name__ == "__main__":
    run()