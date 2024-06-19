""" Usage:
    <file-name> --in=IN_FILE --out=OUT_FILE [--debug]
"""
# External imports
import logging
import pdb
import json
from pprint import pprint
from pprint import pformat
from docopt import docopt
from collections import defaultdict
from operator import itemgetter
from tqdm import tqdm
from typing import List, Dict

# Local imports
from languages.util import GENDER, WB_GENDER_TYPES
#=-----

def calc_f1(precision: float, recall: float) -> float:
    """
    Compute F1 from precision and recall.
    """
    return 2 * (precision * recall) / (precision + recall)


def evaluate_bias(ds: List[str], predicted: List[GENDER]) -> Dict:
    """
    (language independent)
    Get performance metrics for gender bias.
    """

    assert(len(ds) == len(predicted))
    prof_dict = defaultdict(list)
    conf_dict = defaultdict(lambda: defaultdict(lambda: 0))
    total = defaultdict(lambda: 0)
    pred_cnt = defaultdict(lambda: 0)
    correct_cnt = defaultdict(lambda: 0)

    count_unknowns = defaultdict(lambda: 0)

    for (original_gold_gender, word_ind, sent, profession), pred_gender in zip(ds, predicted):
        if pred_gender == GENDER.ignore:
            continue # skip analysis of ignored words

        gold_gender = WB_GENDER_TYPES[original_gold_gender]

        if pred_gender == GENDER.unknown:
            count_unknowns[gold_gender] += 1

        sent = sent.split()
        profession = profession.lower()
        if not profession:
            pdb.set_trace()

        total[gold_gender] += 1

        if pred_gender == gold_gender:
            correct_cnt[gold_gender] += 1

        pred_cnt[pred_gender] += 1

        prof_dict[profession].append((pred_gender, gold_gender))
        conf_dict[gold_gender][pred_gender] += 1

    prof_dict = dict(prof_dict)
    all_total = sum(total.values())
    acc = round((sum(correct_cnt.values()) / all_total) * 100, 1)

    recall_male = round((correct_cnt[GENDER.male] / total[GENDER.male]) * 100, 1)
    prec_male = round((correct_cnt[GENDER.male] / pred_cnt[GENDER.male]) * 100, 1)
    f1_male = round(calc_f1(prec_male, recall_male), 1)

    recall_female = round((correct_cnt[GENDER.female] / total[GENDER.female]) * 100, 1)
    prec_female = round((correct_cnt[GENDER.female] / pred_cnt[GENDER.female]) * 100, 1)
    f1_female = round(calc_f1(prec_female, recall_female), 1)

    output_dict = {"acc": acc,
                   "f1_male": f1_male,
                   "f1_female": f1_female,
                   "unk_male": count_unknowns[GENDER.male],
                   "unk_female": count_unknowns[GENDER.female],
                   "unk_neutral": count_unknowns[GENDER.neutral]}
    

    print(json.dumps(output_dict))


def evaluate_bias_complete(ds: List[str], predicted: List[GENDER]) -> Dict:
    assert(len(ds) == len(predicted))
    prof_dict = defaultdict(list)
    conf_dict = defaultdict(lambda: defaultdict(lambda: 0))
    total = defaultdict(lambda: 0)
    pred_cnt = defaultdict(lambda: 0)
    correct_cnt = defaultdict(lambda: 0)
    count_unknowns = defaultdict(lambda: 0)

    for (gold_gender, word_ind, sent, profession), pred_gender in zip(ds, predicted):
        if pred_gender == GENDER.ignore:
            continue # skip analysis of ignored words
        
        gold_gender = WB_GENDER_TYPES[gold_gender]

        sent = sent.split()
        profession = profession.lower()

        if pred_gender == GENDER.unknown:
            count_unknowns[gold_gender] += 1

        if not profession:
            pdb.set_trace()

        total[gold_gender] += 1

        if pred_gender == gold_gender:
            correct_cnt[gold_gender] += 1

        pred_cnt[pred_gender] += 1

        prof_dict[profession].append((pred_gender, gold_gender))
        conf_dict[gold_gender][pred_gender] += 1

    prof_dict = dict(prof_dict)
    all_total = sum(total.values())
    acc = round((sum(correct_cnt.values()) / all_total) * 100, 2)

    recall_male = round((correct_cnt[GENDER.male] / total[GENDER.male]) * 100, 2)
    prec_male = round((correct_cnt[GENDER.male] / pred_cnt[GENDER.male]) * 100, 2)
    f1_male = round(calc_f1(prec_male, recall_male), 2)

    recall_female = round((correct_cnt[GENDER.female] / total[GENDER.female]) * 100, 2)
    prec_female = round((correct_cnt[GENDER.female] / pred_cnt[GENDER.female]) * 100, 2)
    f1_female = round(calc_f1(prec_female, recall_female), 2)

    print(f"#total = {all_total}; \n acc = {acc}%; f1_male = {f1_male}% (p: {prec_male} / r: {recall_male}); f1_female = {f1_female}% (p: {prec_female} / r: {recall_female})")
    print("Gold distribution: male: {}% ({}), female: {}% ({}), neutral: {}% ({}), unknown: {}% ({})".format(round(percentage(total[GENDER.male], all_total), 2), total[GENDER.male],
                                                                                          round(percentage(total[GENDER.female], all_total), 2), total[GENDER.female],
                                                                                          round(percentage(total[GENDER.neutral], all_total), 2), total[GENDER.neutral],
                                                                                          round(percentage(total[GENDER.unknown], all_total), 2), total[GENDER.unknown]))

    print("Predictions: male: {}%, female: {}%, neutral: {}%, unknown: {}%".format(round((pred_cnt[GENDER.male] / all_total) * 100, 2),
                                                                     round((pred_cnt[GENDER.female] / all_total) * 100, 2),
                                                                     round((pred_cnt[GENDER.neutral] / all_total) * 100, 2),
                                                                     round((pred_cnt[GENDER.unknown] / all_total) * 100, 2)))

    male_prof = [prof for prof, vals in prof_dict.items()
                 if all(pred_gender == GENDER.male
                        for pred_gender
                        in map(itemgetter(0), vals))]

    female_prof = [prof for prof, vals in prof_dict.items()
                   if all(pred_gender == GENDER.female
                          for pred_gender
                          in map(itemgetter(0), vals))]

    neutral_prof = [prof for prof, vals in prof_dict.items()
                    if all(pred_gender == GENDER.neutral
                           for pred_gender
                           in map(itemgetter(0), vals))]

    amb_prof = [prof for prof, vals in prof_dict.items()
                if len(set(map(itemgetter(0), vals))) != 1]



    print(f"male professions = {male_prof}")
    print(f"female professions = {female_prof}")
    print(f"neutral professions = {neutral_prof}")
    print(f"ambiguous professions = {amb_prof}")
    print("Unknown male: {}".format(count_unknowns[GENDER.male]))
    print("Unknown female: {}".format(count_unknowns[GENDER.female]))
    print("Unknown neutral: {}".format(count_unknowns[GENDER.neutral]))

    pprint(conf_dict)

    logging.info("DONE")


def percentage(part, total):
    """
    Calculate percentage.
    """
    return (part / total) * 100

if __name__ == "__main__":
    # Parse command line arguments
    args = docopt(__doc__)
    inp_fn = args["--in"]
    out_fn = args["--out"]
    debug = args["--debug"]

    inp_fn = "mt_gender/data/human/google/pt/pt.pred.csv"
    out_fn = args["--out"]

    
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)


    logging.info("DONE")
