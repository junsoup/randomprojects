import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split
import torch.nn.functional as F

torch.manual_seed(1)

# Loading tensor data
inputData = torch.load('tensor3_1.pt')
print("Loaded tensor")

features3d = inputData['features'].to_dense()
labels3d = inputData['labels']

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)

features = features3d.view(features3d.shape[0], -1).to(torch.float32).to(device)
labels = labels3d.view(labels3d.shape[0], -1).to(torch.int64).to(device)

print("Converted to dense")
del features3d
del labels3d
del inputData
class champPredictor(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(champPredictor, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, hidden_size)
        self.fc4 = nn.Linear(hidden_size, hidden_size)
        self.fc5 = nn.Linear(hidden_size, hidden_size)
        self.fc6 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = torch.relu(self.fc4(x))
        x = torch.relu(self.fc5(x))
        x = self.fc6(x)
        return x

input_size = features.shape[1]
output_size = labels.shape[1]*165
learning_rate = .0005
batch_size = 13675
epochs = 250
hidden_size = 1500

# Building dataset
dataset = TensorDataset(features, labels)

train_size = int(1.0 * len(dataset))
# test_size = len(dataset) - train_size

train_dataset = dataset
# , test_dataset = random_split(dataset, [train_size, test_size])

train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
# test_dataloader = DataLoader(test_dataset, batch_size=1, shuffle=True)

print("Dataset built")

model = champPredictor(input_size, hidden_size, output_size).to(device)
criterion = nn.MSELoss()
optimizer = optim.Adagrad(model.parameters(), lr=learning_rate)

# Training
print("Initating training")
for epoch in range(epochs):
    total_loss = 0.0
    for batch_idx, (inputs, targets) in enumerate(train_dataloader):
        # Zero the gradients
        optimizer.zero_grad()
        # print(targets.tolist())
        
        inputs = inputs.to(torch.float32)
        targets = targets.to(torch.int64)
        # Forward pass
        outputs = model(inputs) #shape batch_size, 825
        outputs = outputs.view(-1,5,165) #shape batch_size, 5, 165
        outputs = F.softmax(outputs, dim=2) #softmax last dim.
        indexedOutput = outputs.gather(2, targets.unsqueeze(2)).squeeze(2) #indexes into last dim for critical elements, shape batch_size, 5

        # Compute the loss
        # Sum all critical values (if element == 1, good prediction, else if near 0, bad prediction)
        loss = -torch.sum(indexedOutput)

        # Backpropagation and optimization
        loss.backward()
        optimizer.step()

        # Accumulate the loss for this batch
        total_loss += loss.item()
        # if (batch_idx + 1) % 10 == 0:
        # print(f'Epoch [{epoch+1}/{epochs}] Batch [{batch_idx+1}/{len(train_dataloader)}] Loss: {loss.item()/batch_size}')
    avg_loss = total_loss / -8.25 / batch_size
    print(f'Epoch, Average Loss, {epoch+1}, {avg_loss:.6f}')

model.eval()

champion_id = (266, 103, 84, 166, 12, 32, 34, 1, 523, 22, 136, 268, 432, 200, 53, 63, 201, 233, 51, 164, 69, 31, 42, 122, 131, 119, 36, 245, 60, 28, 81, 9, 114, 105, 3, 41, 86, 150, 79, 104, 887, 120, 74, 420, 39, 427, 40, 59, 
24, 126, 202, 222, 145, 429, 43, 30, 38, 55, 10, 141, 85, 121, 203, 240, 96, 897, 7, 64, 89, 876, 127, 236, 117, 99, 54, 90, 57, 11, 902, 21, 62, 82, 25, 950, 267, 75, 111, 518, 76, 895, 56, 20, 2, 61, 516, 80, 78, 555, 246, 133, 497, 33, 421, 526, 888, 58, 107, 92, 68, 13, 360, 113, 235, 147, 875, 35, 98, 102, 27, 14, 15, 72, 37, 16, 50, 517, 134, 223, 163, 91, 44, 17, 412, 18, 48, 23, 4, 29, 77, 6, 110, 67, 45, 161, 711, 254, 234, 112, 8, 106, 19, 498, 101, 5, 157, 777, 83, 350, 154, 238, 221, 115, 26, 142, 143)
champion_name = ('Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'AurelionSol', 'Azir', 'Bard', 'Belveth', 'Blitzcrank', 'Brand', 'Braum', 'Briar', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana', 'Draven', 'DrMundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'Fiddlesticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kaisa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'KogMaw', 'KSante', 'Leblanc', 'LeeSin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'MasterYi', 'Milio', 'MissFortune', 'MonkeyKing', 'Mordekaiser', 'Morgana', 'Naafiri', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 'RekSai', 'Rell', 'Renata', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'TahmKench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'TwistedFate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'XinZhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra')
role = ("Top", "Jungle", "Mid", "Bot", "Supp")

sampleInput = torch.zeros(1650, dtype=torch.float32).to(device)
topComp = []

with torch.no_grad():
    output = model(sampleInput)
    outputs = output.view(5,165)
    outputs = F.softmax(outputs, dim=1)
    for i, lane in enumerate(outputs):
        winOrder = {}
        for j, champ in enumerate(lane):
            winOrder[champion_name[j]] = round(float(champ)*100, 2)
        winrateLaneOrdered = sorted( ((v,k) for k,v in winOrder.items()), reverse=True)[:5]
        print(f"{role[i]}:\t{winrateLaneOrdered}")
        topComp.append(winrateLaneOrdered[0])
print("\nSample:", end='\t')
print(topComp)
torch.save(model.state_dict(), 'weights7.pth')
