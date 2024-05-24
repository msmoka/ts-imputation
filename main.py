import argparse
import torch
import datetime
import json
import yaml
import os

from CSDI.main_model import CSDI_Physio
from CSDI.dataset_physio import get_dataloader
from CSDI.utils import train, evaluate

path = "config/base.yaml"
with open(path, "r") as f:
    config = yaml.safe_load(f)

config["model"]["is_unconditional"] = "store_true"
config["model"]["test_missing_ratio"] = 0.1
config["modelfolder"] = ""
config["nsample"] = 100
config["nfold"] = 0
config["device"] = "cuda:0"
config["seed"] = 42

current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
foldername = "./save/physio_fold" + str(config["nfold"]) + "_" + current_time + "/"
print('model folder:', foldername)
os.makedirs(foldername, exist_ok=True)
with open(foldername + "config.json", "w") as f:
    json.dump(config, f, indent=4)

train_loader, valid_loader, test_loader = get_dataloader(
    seed=config["seed"],
    nfold=config["nfold"],
    batch_size=config["train"]["batch_size"],
    missing_ratio=config["model"]["test_missing_ratio"],
)

model = CSDI_Physio(config, "cuda:0").to("cuda:0")

evaluate(model, test_loader, nsample=config["nsample"], scaler=1, foldername=foldername)
