import os
import pickle
import time

import torch

from trainer import trainer


def main():
    start_time = time.time()
    DEBUG = True
    dataset_cache = "./data/cache/SQuAD%s.pkl" % ("_debug" if DEBUG else "")

    if os.path.isfile(dataset_cache):
        dataset = pickle.load(open(dataset_cache,"rb"))
    else:

        train_json = "./data/squad/train-v1.1.json"
        from dataset import SQuAD
        dataset = SQuAD(train_json, debug_mode=DEBUG)
        pickle.dump(dataset, open(dataset_cache, "wb"))

    dataloader = dataset.get_dataloader(5, shuffle=True)

    char_embedding_config = {"embedding_weights": dataset.cv_vec,
                             "padding_idx": dataset.PAD,
                             "update": True, "bidirectional": True,
                             "cell_type": "gru", "output_dim": 300}

    word_embedding_config = {"embedding_weights": dataset.wv_vec,
                             "padding_idx": dataset.PAD,
                             "update": False}

    sentence_encoding_config = {"hidden_size": 75, "num_layers": 3,
                                "bidirectional": True,
                                "dropout": 0.2, }

    pair_encoding_config = {"hidden_size": 75, "num_layers": 3, "bidirectional": True,
                            "dropout": 0.2, "gated": True, "mode":"GRU",
                            "rnn_cell": torch.nn.GRUCell, "attn_size":75, "residual": False}

    self_matching_config = {"hidden_size": 75, "num_layers": 3, "bidirectional": True,
                            "dropout": 0.2, "gated": True, "mode":"GRU",
                            "rnn_cell": torch.nn.GRUCell, "attn_size":75, "residual": False}

    pointer_config = {"hidden_size": 75, "num_layers": 3,"dropout": 0.2,"residual": False, "rnn_cell": torch.nn.GRUCell}

    trainer(char_embedding_config, dataloader, pair_encoding_config, pointer_config, self_matching_config,
            sentence_encoding_config, start_time, word_embedding_config)


if __name__ == "__main__":
    main()
