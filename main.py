import sys


class Gate:
    def __init__(self, gate_type, inputs, outputs, delays, areas):
        self.gate_type = gate_type  # encoding the type of gate
        self.inputs = inputs  # inputs to the gate
        self.outputs = outputs  # outputs of the gate
        self.delay = delays  # encoding the delay
        self.area = areas  # encoding the area
        self.prev = []  # to store the previous gates


def input():
    intput_str = ""
    input_filename = str(sys.argv[2])
    with open(input_filename, 'r') as file:
        intput_str = file.read()

    gate_delay_str = ""
    delay_filename = str(sys.argv[3])
    with open(delay_filename, 'r') as file:
        gate_delay_str = file.read()

    output_file = str(sys.argv[4])

    return intput_str, gate_delay_str, output_file


def input_b():
    intput_str = ""
    input_filename = str(sys.argv[2])
    with open(input_filename, 'r') as file:
        intput_str = file.read()

    gate_delay_str = ""
    delay_filename = str(sys.argv[3])
    with open(delay_filename, 'r') as file:
        gate_delay_str = file.read()

    delay_constraint_file = str(sys.argv[4])
    with open(delay_constraint_file, 'r') as file:
        delay_constraint = file.read()

    min_area_file = str(sys.argv[5])

    return intput_str, gate_delay_str, delay_constraint, min_area_file

def formatted_input():
    input_spice, gate_delay_str, output_file = input()

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

    return formatted_input_lines, formatted_delay_lines, output_file

def formatted_input_b():
    input_spice, gate_delay_str, delay_constraint, output_file = input_b()

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

    # ---------------- delay contraint ----------------------
    delay_cons_val = int(delay_constraint)

    return formatted_input_lines, formatted_delay_lines, delay_cons_val, output_file



def parse_input(lines, delays_list):
    delays_dict = {}  # dict for later use {gate_type: delay}
    area_dict = {}  # dict for later use {gate_type: area}
    iterator = 0
    while (iterator < len(delays_list)):
        temp_1 = delays_list[iterator].split(" ")
        temp_2 = delays_list[iterator+1].split(" ")
        temp_3 = delays_list[iterator+2].split(" ")
        gate = temp_1[1]
        delays = [float(temp_1[2]), float(temp_2[2]), float(temp_3[2])]
        areas = [float(temp_1[3]), float(temp_2[3]), float(temp_3[3])]
        delays_dict[gate] = delays
        area_dict[gate] = areas
        iterator += 3

    primary_inputs = lines[0].split()[1:]
    primary_outputs = lines[1].split()[1:]

    gates = []  # array of Gate(s)
    for line in lines[3:]:
        tokens = line.split()
        gate_type = tokens[0]
        inputs = tokens[1:-1]
        output = tokens[-1]
        if (gate_type == "DFF"):
            gates.append(
                Gate(gate_type,  inputs, output, [0, 0, 0], [0, 0, 0]))
        else:
            gates.append(Gate(gate_type,  inputs, output,
                         delays_dict[gate_type], area_dict[gate_type]))

    # primary_inputs is an array of primary inputs
    # primary_outputs is an array of primary outputs
    # internal_signals is an array of internal signals
    # the array of gates
    return primary_inputs, primary_outputs, gates


def max_delay(list_gate, dict):
    list_delay = []
    for gate_input in list_gate:
        list_delay.append(dict[gate_input])
    return max(list_delay)


def main_a():
    input_spice, gate_delay_str, output_file = formatted_input()
    primary_inputs, primary_outputs, gates = parse_input(
        input_spice, gate_delay_str
    )
    dict = {}  # signal vs time delay
    for signal in primary_inputs:
        dict[signal] = 0

    to_compare = []
    for gate in gates:
        if (gate.gate_type == "DFF"):
            dict[gate.outputs[0]] = 0
        else:
            pass

    for gate in gates:
        if (gate.gate_type == "DFF"):
            to_compare.append(dict[gate.inputs[0]])
            dict[gate.outputs[0]] = 0
        else:
            dict[gate.outputs] = max_delay(gate.inputs, dict) + min(gate.delay)


    for outputs in primary_outputs:
        to_compare.append(dict[outputs])

    output_a = str(max(to_compare))
    with open(output_file, 'w') as file:
        file.write(output_a+'\n')


def main_b():
    input_spice, gate_delay_str, delay_constraint, output_file = formatted_input_b()
    primary_input, primary_output, gates = parse_input(
        input_spice, gate_delay_str
    )
    dict = {}
    


def main():
    if sys.argv[1] == "A":
        main_a()
    elif sys.argv[1] == "B":
        main_b()


if __name__ == "__main__":
    main()
