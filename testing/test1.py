import pickle

from testing import xor_agent

file_path = "C:\\Users\\USER\\PycharmProjects\\AIing\\xor_network.pkl"

# Now, you can load the instance back from the file
with open(file_path, "rb") as file:
    loaded_network = pickle.load(file)\

predictions = []
for i in range(len(xor_agent.test_inputs)):
    predictions.append(loaded_network.predict(xor_agent.test_inputs[i]))
print(f"Predictions: {predictions}")
print(xor_agent.test_outputs)