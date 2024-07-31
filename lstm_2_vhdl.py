from Communication import Communication

class LSTM2VHDL():
    def __init__(self, nbits, input_range, accuracy, dp, forget_data, input_data, candidate_data, output_data, n_inputs, input_shape, weight_shape):
        comms = Communication(nbits, input_range, accuracy, dp, forget_data, input_data, candidate_data, output_data, n_inputs, input_shape, weight_shape)
        comms.writeToFle()

if __name__ == "__main__":
    data = [
{'input_weights': 1048, 'gate_biases': 993998, 'short_weights': 667},
{'input_weights': -1187, 'gate_biases': 489871, 'short_weights': 777},
{'input_weights': 869, 'gate_biases': -256319, 'short_weights': 1194},
{'input_weights': 1297, 'gate_biases': 548073, 'short_weights': 235}]
    nbits = 10
    model_conv = LSTM2VHDL(nbits, [-1,10], 0.01, 3, data[0], data[2], data[1], data[3], 4, [1, 1], [1, 1])