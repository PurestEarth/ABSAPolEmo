import argparse
from utils.data_utils import load_from_folder
from models.lstm import LSTM, Trainer

from models.Transformers import Transformers


def main(args):
    if args.model == 'LSTM':
        x_train, y_train = load_from_folder(args.input)
        x_valid, y_valid = load_from_folder(args.valid)
        uniq_labels = list(set(i for j in y_train for i in j))
        ignored_label = "IGNORE"
        label_map = {label: i for i, label in enumerate(uniq_labels, 1)}
        label_map[ignored_label] = 0
        print(label_map)
        print(y_train[0])
        biLSTMCRF = LSTM(n_labels=len(uniq_labels), 
                            embedding_path=args.embedding,
                            hidden_size=1024, 
                            input_size=args.train_batch_size*args.max_seq_length
                            )
        trainer = Trainer()
        trainer.train(biLSTMCRF, x_train, y_train, x_valid=x_valid, y_valid=y_valid, label_map=label_map, epochs=args.epochs, train_batch_size=args.train_batch_size, output_dir=args.output,
                      gradient_accumulation_steps=args.gradient_accumulation_steps, seed=args.seed, max_seq_length=args.max_seq_length)
        #if not os.path.exists(args.output):
        #    os.makedirs(args.output)
        #biLSTMCRF.save(args.output)
    else:
        transformers = Transformers()
        transformers.train(
            output_dir=args.output,
            train_batch_size=args.train_batch_size, 
            gradient_accumulation_steps=args.gradient_accumulation_steps, 
            seed=args.seed,
            max_seq_length=args.max_seq_length,
            epochs=args.epochs, 
            data_path=args.input, 
            pretrained_path=args.pretrained, 
            valid_path=args.valid,
            model_name=args.model
        )


def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert set of IOB files into a single json file in PolEval 2018 NER format')
    parser.add_argument('--input', required=True, metavar='PATH', help='path to input')
    parser.add_argument('--output', required=True, metavar='PATH', help='directory where model shall be saved')
    parser.add_argument('--valid', metavar='PATH', help='directory to validation data')
    parser.add_argument('--model', required=True, metavar='PATH', help='name of the model to train - LSTM | BERT | Reformer')
    parser.add_argument('--embedding', metavar='PATH', help='path to embeddings')
    parser.add_argument('--pretrained', metavar='PATH', help='path to pretrained model')
    parser.add_argument('--seed', type=int, default=44, help='seed')
    parser.add_argument('--max_seq_length', type=int, default=128, help='max sequence length')
    parser.add_argument('--gradient_accumulation_steps', type=int, default=1, help='gradient accumulation steps')
    parser.add_argument('--epochs', required=True, default=32, type=int, metavar='num', help='number of epochs')
    parser.add_argument('--char', default=True, help='use char embedding built from training data')
    parser.add_argument('-g', nargs='+', help='which GPUs to use')
    parser.add_argument("--train_batch_size", default=32, type=int, help="Total batch size for training.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    #try:
    main(args)
    #except ValueError as er:
        #rint("[ERROR] %s" % er)