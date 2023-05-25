import training
from model import CubeModel
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, SubsetRandomSampler
import torch.optim
from sklearn.model_selection import KFold
import numpy as np

num_folds = 4

indices = np.arange(len(training.dataset))
kfold = KFold(n_splits=num_folds, shuffle=True)

for fold, (train_indices, test_indices) in enumerate(kfold.split(indices)):
    print()
    print(f'Fold {fold}:')
    print('\tTrain samples:', len(train_indices))
    print('\tTest samples:', len(test_indices))

    model = CubeModel().to(training.PYTORCH_DEVICE)
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=training.LEARNING_RATE)

    # Create samplers for the training and test sets
    train_sampler = SubsetRandomSampler(train_indices)
    test_sampler = SubsetRandomSampler(test_indices)

    train_loader = DataLoader(
            training.dataset,
            batch_size=training.BATCH_SIZE,
            sampler=train_sampler,
    )
    test_loader = DataLoader(
            training.dataset,
            batch_size=training.BATCH_SIZE,
            sampler=test_sampler,
    )

    # Train the model using training data
    for epoch in range(training.EPOCHS):
        print('Training epoch:', epoch)
        model = model.train()
        for batch, (X, y) in enumerate(train_loader):
            if batch % 200 == 0:
                print('\tTraining with batch:', batch)
            X = X.to(training.PYTORCH_DEVICE)
            y = y.to(training.PYTORCH_DEVICE)
            
            pred = model(X)
            loss = criterion(pred, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    # Test with test set
    model = model.eval()
    with torch.no_grad():
        print('Testing')
        total_samples, correct_samples = 0, 0
        for batch, (X, y) in enumerate(test_loader):
            if batch % 200 == 0:
                print('\tTesting with batch:', batch)
            X = X.to(training.PYTORCH_DEVICE)
            y = y.to(training.PYTORCH_DEVICE)

            pred = model(X)

            _, predicted = torch.max(pred.data, 1)
            total_samples += y.size(0)
            correct_samples += (predicted == y).sum().item()
        acc = correct_samples * 100 / total_samples
        print(f'Test accuracy: {acc:.4f} ({correct_samples} / {total_samples}')


