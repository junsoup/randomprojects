import pandas as pd
import torch

data = pd.read_csv("outSim.txt")
champion_id = [266, 103, 84, 166, 12, 32, 34, 1, 523, 22, 136, 268, 432, 200, 53, 63, 201, 233, 51, 164, 69, 31, 42, 122, 131, 119, 36, 245, 60, 28, 81, 9, 114, 105, 3, 41, 86, 150, 79, 104, 887, 120, 74, 420, 39, 427, 40, 59, 
24, 126, 202, 222, 145, 429, 43, 30, 38, 55, 10, 141, 85, 121, 203, 240, 96, 897, 7, 64, 89, 876, 127, 236, 117, 99, 54, 90, 57, 11, 902, 21, 62, 82, 25, 950, 267, 75, 111, 518, 76, 895, 56, 20, 2, 61, 516, 80, 78, 555, 246, 133, 497, 33, 421, 526, 888, 58, 107, 92, 68, 13, 360, 113, 235, 147, 875, 35, 98, 102, 27, 14, 15, 72, 37, 16, 50, 517, 134, 223, 163, 91, 44, 17, 412, 18, 48, 23, 4, 29, 77, 6, 110, 67, 45, 161, 711, 254, 234, 112, 8, 106, 19, 498, 101, 5, 157, 777, 83, 350, 154, 238, 221, 115, 26, 142, 143]

# Convert Pandas DataFrames to NumPy arrays
features = data.iloc[:, :10]
labels = data.iloc[:, -5:]
features = features.to_numpy()
labels = labels.to_numpy()
# labels = torch.from_numpy(labels)


print("Created dense")

# Number of classes for one-hot encoding (165 in your case)
num_classes = 165

# Function to convert labels to one-hot vectors
def one_hot_encode(label_array, num_classes):
    num_samples, num_columns = label_array.shape
    one_hot_labels = torch.zeros((num_samples, num_columns, num_classes), dtype=torch.int16)

    for i in range(num_samples):
        for j in range(num_columns):
            if i % 10 == 0:
                print(i)
            
            if int(label_array[i,j]) == 0:
                continue
            label_index = champion_id.index(int(label_array[i, j]))
            one_hot_labels[i, j, label_index] = 1

    return one_hot_labels


for i in range(labels.shape[0]):
    for j in range(labels.shape[1]):
        labels[i][j] = champion_id.index(labels[i][j])
labels = torch.from_numpy(labels)
# Encode as one-hot vectors
features = one_hot_encode(features, num_classes)


        
        

# labels = one_hot_encode(labels, num_classes)
# print(type(one_hot_features))
print(features.shape)
# print(type(one_hot_labels))
print(labels.shape)
# f_indicies = torch.nonzero(features, as_tuple=False)
fsparse = features.to_sparse()
# l_indicies = torch.nonzero(labels, as_tuple=False)
# lsparse = labels.to_sparse()

tensor_dict = {
    'features': fsparse,
    'labels': labels
}
torch.save(tensor_dict, "tensor3_1.pt")
