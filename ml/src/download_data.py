import os
import kagglehub


def download_dataset():
    print("Downloading dataset...")

    path = kagglehub.dataset_download(
        "ibrahimelsayed182/plane-ticket-price"
    )

    print(f"\nDataset downloaded to:")
    print(path)

    print("\nFiles found:")
    for file in os.listdir(path):
        print(f" - {file}")

    return path


if __name__ == "__main__":
    download_dataset()