import argparse
import logging
import sys
from collections import defaultdict
import random

from rich.console import Console

# +
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(project_root)
# -

from newpotato.datasets.food_disease import load_and_map_fd
from newpotato.datasets.lsoie import load_and_map_lsoie
from newpotato.extractors.graph_extractor import GraphBasedExtractor
from newpotato.evaluate.evaluate import Evaluator


class ExtractorEvaluator(Evaluator):
    def __init__(self, extractor, gold_data):
        super(ExtractorEvaluator, self).__init__()
        self.extractor = extractor
        self.gold_data = gold_data

    def infer_triplets(self, sen):
        preds = self.extractor.infer_triplets(sen)
        return preds

    def gen_texts_with_gold_triplets(self):
        for sen, triplet_list in self.gold_data.items():
            yield sen, [triplet for triplet, is_true in triplet_list if is_true]


def get_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-t", "--data_type", default=None, type=str)
    parser.add_argument("-i", "--input_file", default=None, type=str)
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-e", "--events_file", default=None, type=str)
    parser.add_argument("-r", "--which_rel", default=None, type=str)
    parser.add_argument("-tf","--test_file", default=None, type=str)
    parser.add_argument("-f","--input_folder", default=None, type=str)
    return parser.parse_args()


def main():
    args = get_args()
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s : %(module)s (%(lineno)s) - %(levelname)s - %(message)s",
        force=True,
    )
    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    console = Console()
    extractor = GraphBasedExtractor(default_relation=args.which_rel)
    
    train_file = args.input_file
    test_file = args.test_file if args.test_file else train_file
    
    if args.input_folder:
        train_file = f"data/{args.input_folder}/train.csv"
        test_file = f"data/{args.input_folder}/val.csv"
    
    
    if args.data_type == 'fd':
        logging.info(f"loading train data from {train_file}...")
        
        train_data = {
            sen: [(triplet, True) for triplet in triplets]
            for sen, triplets in load_and_map_fd(train_file, extractor, args.which_rel)
        }

        logging.info(f"loading test data from {test_file}...")
        test_data = {
            sen: [(triplet, True) for triplet in triplets]
            for sen, triplets in load_and_map_fd(test_file, extractor, args.which_rel)
        }
        
    elif args.data_type == 'lsoie':
        gold_data = defaultdict(list)
        for sen, triplet in load_and_map_lsoie(args.input_file, extractor):
            gold_data[sen].append((triplet, True))
        train_data = gold_data
        test_data = gold_data
    else:
        raise ValueError(f'unknown data type: {args.data_type}')
      
    
    # training
    logging.info("training...")
    extractor.get_rules(train_data)
    
    extractor.print_rules(console)

    # evaluation
    logging.info("evaluating...")
    evaluator = ExtractorEvaluator(extractor, test_data)

    results = evaluator.get_results()
    for key, value in results.items():
        print(f"{key}: {value}")

    if args.events_file is not None:
        if args.events_file == "-":
            evaluator.write_events(sys.stdout)
        else:
            evaluator.write_events_to_file(args.events_file)

if __name__ == "__main__":
    main()
