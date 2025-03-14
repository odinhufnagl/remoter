import argparse
from train import train_model


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train model.")
    parser.add_argument(
        "--epochs",
        type=str,
        required=True,
        help="How many epochs to train the model",
    )
    args = parser.parse_args()
    train_model(int(args.epochs))
