from model import CubeModel
import torch
import torch.nn as nn
import cubes_dataset
import os

PYTORCH_DEVICE = os.getenv('PYTORCH_DEVICE', 'cuda')
print('[pytorch] Using device:', PYTORCH_DEVICE)

assert torch.cuda.is_available(), 'CUDA is not available'

model = CubeModel().to(PYTORCH_DEVICE)

# Hyper-parameters
LEARNING_RATE = 0.001
BATCH_SIZE = 2000
EPOCHS = 20

print('[pytorch] Using hyper-parameters:')
print('[pytorch] LEARNING_RATE:', LEARNING_RATE)
print('[pytorch] BATCH_SIZE:', BATCH_SIZE)
print('[pytorch] EPOCHS:', EPOCHS)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

# Train the model
def train_loop(model, loss_fn, optimizer):
    batch = 0
    X, y = cubes_dataset.load_cubes_dataset_as_tensor(batch, BATCH_SIZE)

    while len(X) > 0:
        batch += BATCH_SIZE

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

        if batch % 1000 == 0 or BATCH_SIZE > 1000:
            loss = loss.item()
            print(f"loss: {loss:>7f}  [batch={batch}]")
        
        # Load next batch
        X, y = cubes_dataset.load_cubes_dataset_as_tensor(batch, BATCH_SIZE)

for epoch in range(EPOCHS):
    print(f"Epoch {epoch+1}\n-------------------------------")
    train_loop(model, criterion, optimizer)

# Save the model checkpoint
torch.save(model, 'model.ckpt')