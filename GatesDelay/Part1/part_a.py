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
    for outputs in primary_outputs:
        output.append(f"{outputs} {(dict[outputs]):.3f}")
    with open("output_delays.txt", 'w') as file:
        for item in output:
            file.write(item + '\n')



def main():
    input_spice, gate_delay_str = formatted_input()
    primary_inputs, primary_outputs, gates = parse_input(
        input_spice, gate_delay_str)
    dict = {}  # signal vs time delay
    for signal in primary_inputs:
        dict[signal] = 0

    for gate in gates:
        dict[gate.outputs] = max_delay(gate.inputs, dict) + gate.delay

    output(dict, primary_outputs)


if __name__ == "__main__":
    main()
