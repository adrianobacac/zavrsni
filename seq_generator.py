import os
import argparse
import random
import json
from contextlib import nested


def get_parser():
    parser = argparse.ArgumentParser(description='Simple sequence generator')
    parser.add_argument(
        '-d', '--dest', action="store", default="output", help="Destination folder")
    parser.add_argument('config', action="store", help="JSON config file")
    return parser


def gen_mutated_seq(seq, error_prob, substitution_only):
    def substitution(nucl):
        short__nucls = _NUCLS[:]
        short__nucls.remove(nucl)
        return short__nucls[random.randint(0, len(short__nucls) - 1)], "s"

    def deletion(nucl):
        return "", "d"

    def addition(nucl):
        side = random.randint(0, 1)
        if side == 0:
            return _NUCLS[random.randint(0, len(_NUCLS) - 1)] + nucl, "a"
        else:
            return nucl + _NUCLS[random.randint(0, len(_NUCLS) - 1)], "a"

    options = [deletion, addition, substitution]
    report = {}
    new_seq = []
    for i, nucl in enumerate(seq):
        if error_prob > random.uniform(0.0, 1.0):
            if substitution_only:
                new_nucl, sym = substitution(nucl)
                report.update({i: [sym, nucl, new_nucl]})
            else:
                new_nucl, sym = options[
                    random.randint(0, len(options) - 1)](nucl)
                report.update({i: [sym, nucl, new_nucl]})
        else:
            new_nucl = nucl
        new_seq.append(new_nucl)
    return "".join(new_seq), report


def main():
    args = get_parser().parse_args()

    with open(args.config) as json_file:
        try:
            config = json.load(json_file)
        except ValueError:
            print "Config file is not in json format"
            exit()
    if not all(param in config for param in ("lenghts", "error_probs", "seq_counts", "substitution_only")):
        print "Config file missing parameters"
        exit()

    if not os.path.isdir(args.dest):
        os.mkdir(args.dest)
    """
    Stvaranje baznih sekvenci
    """
    for lenght in config['lenghts']:
        with open("%s/len_%d_base.fa" % (args.dest, lenght), 'w') as fout:
            for i in xrange(lenght):
                nucl = _NUCLS[random.randint(0, len(_NUCLS) - 1)]
                fout.write(nucl)
    """
    Stvaranje mutiranih sekvenci
    """
    substitution_only = config["substitution_only"]
    with open("%s/all.fa" % args.dest, "w") as fout_all:
        for lenght in config['lenghts']:
            for (seq_count, error_prob) in zip(config["seq_counts"], config["error_probs"]):
                for i in xrange(seq_count):
                    with nested(
                        open("%s/len_%d_base.fa" % (args.dest, lenght), 'r'),
                        open("%s/len_%d_p_%g_%d.fa" %
                             (args.dest, lenght, error_prob, i + 1), 'w')
                    ) as (fin, fout):
                        seq = fin.read()
                        mutated_seq, report = gen_mutated_seq(
                            seq, error_prob, substitution_only)
                        title = ">p_%g_%d%s\n" % (error_prob, i + 1, json.dumps(report))
                        fout.write(title)
                        fout.write(mutated_seq + "\n")

                        fout_all.write(title)
                        fout_all.write(mutated_seq + "\n")

if __name__ == '__main__':
    _NUCLS = ['A', 'C', 'G', 'T']
    main()
