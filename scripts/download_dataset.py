"""
Script to download Credit Card Fraud Detection dataset from Kaggle.
Requires Kaggle API credentials (kaggle.json).
"""
import os
from kaggle.api.kaggle_api_extended import KaggleApi

def download_kaggle_dataset():
    api = KaggleApi()
    api.authenticate()
    
    dataset = "mlg-ulb/creditcardfraud"
    download_path = "."
    
    print(f"Downloading dataset: {dataset}")
    api.dataset_download_files(dataset, path=download_path, unzip=True)
    print("Dataset downloaded successfully!")

if __name__ == "__main__":
    download_kaggle_dataset()
