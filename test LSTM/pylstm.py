import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def lstm_step(x_t, h_prev, C_prev, W_f_x, W_f_h, b_f, W_i_x, W_i_h, b_i, W_C_x, W_C_h, b_C, W_o_x, W_o_h, b_o):
    # Forget gate
    f_t = sigmoid(np.dot(x_t, W_f_x) + np.dot(h_prev, W_f_h) + b_f)

    # Input gate
    i_t = np.tanh(np.dot(x_t, W_i_x) + np.dot(h_prev, W_i_h) + b_i)

    # Candidate values
    C_tilde = sigmoid(np.dot(x_t, W_C_x) + np.dot(h_prev, W_C_h) + b_C)

    # Cell state
    C_t = f_t * C_prev + i_t * C_tilde
    
    # Output gate
    o_t = sigmoid(np.dot(x_t, W_o_x) + np.dot(h_prev, W_o_h) + b_o)
    
    # Hidden state
    h_t = o_t * np.tanh(C_t)
    print(h_t)
    
    return h_t, C_t

# Sample weights and biases
#forget gate weights and biases
W_f_x = np.array([[0.5, -0.1], [0.3, 0.2]])
W_f_h = np.array([[0.1, -0.3], [-0.2, 0.1]])
b_f = np.array([0.1, -0.2])

# input gate weights and biases
W_i_x = np.array([[0.6, -0.2], [-0.1, 0.3]])
W_i_h = np.array([[0.2, -0.4], [0.3, 0.1]])
b_i = np.array([-0.1, 0.1])

# candidate gate weights and biases
W_C_x = np.array([[0.4, -0.3], [0.3, 0.1]])
W_C_h = np.array([[0.2, 0.5], [0.1, -0.2]])
b_C = np.array([0.1, -0.1])

#output gate weights and biases
W_o_x = np.array([[0.5, 0.1], [-0.3, 0.2]])
W_o_h = np.array([[0.4, -0.2], [0.2, 0.3]])
b_o = np.array([0.0, 0.1])

# Input sequence (time steps x features)
X = np.array([[1.0, 0.5], [0.5, 1.0], [1.0, 1.0]])

# Initial cell state and hidden state
C_t = np.zeros(2)
h_t = np.zeros(2)

# Apply LSTM step by step
outputs = []
for t in range(X.shape[0]):
    x_t = X[t]
    h_t, C_t = lstm_step(x_t, h_t, C_t, W_f_x, W_f_h, b_f, W_i_x, W_i_h, b_i, W_C_x, W_C_h, b_C, W_o_x, W_o_h, b_o)
    outputs.append((h_t, C_t))
    

# Extract the final hidden state as the prediction
final_hidden_state = h_t
outputs, final_hidden_state


