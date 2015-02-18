import argparse

def dice_coefficient(a, b, k=2):
    if not len(a) or not len(b):
        return 0.0
    if len(a) == 1:
        a = a + u'.'
    if len(b) == 1:
        b = b + u'.'

    a_bigram_list = []
    for i in range(len(a) - (k - 1)):
        a_bigram_list.append(a[i:i + k])
    b_bigram_list = []
    for i in range(len(b) - 1):
        b_bigram_list.append(b[i:i + k])

    a_bigrams = set(a_bigram_list)
    b_bigrams = set(b_bigram_list)
    overlap = len(a_bigrams & b_bigrams)
    dice_coeff = overlap * 2.0 / (len(a_bigrams) + len(b_bigrams))
    return dice_coeff


def get_parser():
    parser = argparse.ArgumentParser(
        description='Implementation of Sorensen-Dice coefficient')
    parser.add_argument('str1',  help="First string")
    parser.add_argument('str2',  help="Second string")
    return parser


def main():
    args = get_parser().parse_args()
    print dice_coefficient(args.str1, args.str2, 3)

if __name__ == '__main__':
    main()
