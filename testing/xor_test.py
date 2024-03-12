import pickle

from testing import xor_agent

file_path = "C:\\Users\\USER\\PycharmProjects\\AIing\\networks\\xor_network.pkl"
# file_path = "C:\\Users\\USER\\PycharmProjects\\AIing\\save_network_2.pkl"

# Now, you can load the instance back from the file
with open(file_path, "rb") as file:
    loaded_network = pickle.load(file)\

predictions = []
for i in range(len(xor_agent.test_inputs)):
    predictions.append(loaded_network.predict(xor_agent.test_inputs[i]))
print(f"Predictions: {predictions}")
print(xor_agent.test_outputs)