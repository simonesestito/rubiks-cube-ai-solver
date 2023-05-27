from model import CubeModel
import torch
import torch.nn as nn
import cubes_dataset
import os

PYTORCH_DEVICE = os.getenv('PYTORCH_DEVICE', 'cuda')
print('[pytorch] Using device:', PYTORCH_DEVICE)

assert PYTORCH_DEVICE != 'cuda' or torch.cuda.is_available(), 'CUDA is not available'

# Load model, if present
if os.path.isfile('model.ckpt'):
    print('[pytorch] Loading model from checkpoint...')
    model = torch.load('model.ckpt')
else:
    print('[pytorch] Creating new model from SCRATCH...')
    model = CubeModel()
model = model.to(PYTORCH_DEVICE)
print(model)

# Hyper-parameters
LEARNING_RATE = 0.01
BATCH_SIZE = 3000
EPOCHS = 5

print('[pytorch] Using hyper-parameters:')
print('[pytorch] LEARNING_RATE:', LEARNING_RATE)
print('[pytorch] BATCH_SIZE:', BATCH_SIZE)
print('[pytorch] EPOCHS:', EPOCHS)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

dataset = cubes_dataset.CubesDataloader()
dataloader = torch.utils.data.DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# Train the model
def train_loop(model, loss_fn, optimizer):
    model = model.train()

    total_samples, correct_samples = 0, 0
    for batch, (X, y) in enumerate(dataloader):
        # Move tensors to the configured device
        X = X.to(PYTORCH_DEVICE)
        # Compute prediction and loss
        pred = model(X)
        y = y.to(PYTORCH_DEVICE)
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Compute accuracy
        _, predicted = torch.max(pred.data, 1)
        total_samples += y.size(0)
        correct_samples += (predicted == y).sum().item()

        if batch % 200 == 0:
            loss = loss.item()
            print(f"loss: {loss:>7f}  [batch={batch:04d}] - Batch accuracy: {correct_samples/total_samples*100:.4f}% ({correct_samples}/{total_samples})")
            total_samples, correct_samples = 0, 0

if __name__ == '__main__':
    for epoch in range(EPOCHS):
        print('-------------------------------')
        print(f'Epoch {epoch+1}')
        train_loop(model, criterion, optimizer)

    # Save the model checkpoint
    torch.save(model, 'model.ckpt')
