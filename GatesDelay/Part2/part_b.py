# Gate class


class Gate:
    def __init__(self, gate_type, inputs, outputs, delay):
        self.gate_type = gate_type  # encoding the type of gate
        self.delay = delay  # encoding the delay
        self.inputs = inputs  # inputs to the gate
        self.outputs = outputs  # outputs of the gate
        self.prev = []  # to store the previous gates


def max_delay(list_gate, dict):
    list_delay = []
    for gate_input in list_gate:
        list_delay.append(dict[gate_input])
    return max(list_delay)


def parse_input(lines, delays_list):
    delays_dict = {}  # dict for later use {gate_type: delay}
    for gate_delays in delays_list:
        temp = gate_delays.split(" ")
        gate = temp[0]
        delay = temp[1]
        delays_dict[gate] = float(delay)

    primary_inputs = lines[0].split()[1:]
    primary_outputs = lines[1].split()[1:]

    gates = []  # array of Gate(s)
    for line in lines[3:]:
        tokens = line.split()
        gate_type = tokens[0]
        inputs = tokens[1:-1]
        output = tokens[-1]
        gates.append(Gate(gate_type,  inputs, output, delays_dict[gate_type]))

    # primary_inputs is an array of primary inputs
    # primary_outputs is an array of primary outputs
    # internal_signals is an array of internal signals
    # the array of gates
    return primary_inputs, primary_outputs, gates


def input():
    intput_str = ""
    input_filename = "circuit.txt"
    with open(input_filename, 'r') as file:
        intput_str = file.read()

    gate_delay_str = ""
    delay_filename = "gate_delays.txt"
    with open(delay_filename, 'r') as file:
        gate_delay_str = file.read()

    return intput_str, gate_delay_str


def formatted_input():
    input_spice, gate_delay_str = input()

    # ------------------- input_spice -----------------------
    # list that breaks the input into elements
    input_lines = input_spice.strip().split('\n')
    formatted_input_lines = []
    for line in input_lines:
        try:
            if not line[0]:
                continue
            elif line[0] == '/' and line[1] == '/':
                continue
            else:
                formatted_input_lines.append(line)
        except:
            continue

    # ------------------- delay -------------------------------
    delay_lines = gate_delay_str.strip().split('\n')
    formatted_delay_lines = []
    for line in delay_lines:
        try:
            if not line[0]:
                continue
            elif line[0] == '/' and line[1] == '/':
                continue
            else:
                formatted_delay_lines.append(line)
        except:
            continue

    return formatted_input_lines, formatted_delay_lines


def output(dict, primary_outputs):
    output = []
    not_possible = True
    for outputs in primary_outputs:
        if dict[outputs] != 0:
            not_possible = False
    
    if not not_possible:
        for outputs in primary_outputs:
            output.append(f"{outputs} {(dict[outputs])}")
        with open("input_delays.txt", 'w') as file:
            for item in output:
                file.write(item + '\n')
    else:
        with open("input_delays.txt", 'w') as file:
            file.write("not possible")

def input_b():
    input_output = ""
    filename = "required_delays.txt"
    with open(filename, 'r') as file:
        input_output = file.read()

    output = input_output.strip().split('\n')
    required_output = {}
    for line in output:
        try:
            if not line[0]:
                continue
            elif line[0] == '/' and line[1] == '/':
                continue
            else:
                required_output[line[0]] = int(line[2:])
        except:
            continue

    return required_output


def part_a():
    input_spice, gate_delay_str = formatted_input()
    primary_inputs, primary_outputs, gates = parse_input(
        input_spice, gate_delay_str)
    dict = {}  # signal vs time delay
    for signal in primary_inputs:
        dict[signal] = 0

    for gate in gates:
        dict[gate.outputs] = max_delay(gate.inputs, dict) + gate.delay

    return dict, primary_inputs, primary_outputs, gates


def final_check(dict_a, ans_dict, primary_inputs, primary_outputs, gates):
    input_spice, gate_delay_str = formatted_input()
    primary_inputs, primary_outputs, gates = parse_input(
        input_spice, gate_delay_str)

    # modified dict_a will be passed
    dict = {}  # signal vs time delay
    for signal in primary_inputs:
        dict[signal] = dict_a[signal]

    for gate in gates:
        dict[gate.outputs] = max_delay(gate.inputs, dict) + gate.delay
    print(dict)
    check = True
    for output in primary_outputs:
        if dict[output] != ans_dict[output]:
            check = False
            break
    return check


def primary_check(dict_a, ans_dict, primary_inputs, primary_outputs, gates):
    # checking if the case of having the only one primary input as non zero helps
    diff = -1
    passed = True
    for output in primary_outputs:
        if diff == -1:
            diff = ans_dict[output] - dict_a[output]
        elif diff != ans_dict[output] - dict_a[output]:
            passed = False

    if passed:
        for inputs in primary_inputs:
            dict_a[inputs] = diff
            check = final_check(
                dict_a, ans_dict, primary_inputs, primary_outputs, gates)
            if check:
                return dict_a
            else:
                dict_a[inputs] = 0
    else:
        return dict_a


def secondary_check(dict_a, ans_dict, primary_inputs, primary_outputs, gates):
    upper_bound = max(ans_dict.values())
    for a in range(upper_bound):
        for b in range(upper_bound):
            dict_a[primary_inputs[0]] = a
            dict_a[primary_inputs[1]] = b
            check = final_check(dict_a, ans_dict, primary_inputs, primary_outputs, gates)
            if check:
                return dict_a
            else:
                dict_a[primary_inputs[0]] = 0
                dict_a[primary_inputs[1]] = 0
    return dict_a


def main():
    dict_a, primary_inputs, primary_outputs, gates = part_a()
    ans_dict = input_b()
    dict_a = primary_check(
        dict_a, ans_dict, primary_inputs, primary_outputs, gates)
    if final_check(dict_a, ans_dict, primary_inputs, primary_outputs, gates):
        output(dict_a, primary_inputs)
    else:
        dict_a = secondary_check(
            dict_a, ans_dict, primary_inputs, primary_outputs, gates)
        output(dict_a, primary_inputs)


if __name__ == "__main__":
    main()
