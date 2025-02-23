import argparse


def main():
    parser = argparse.ArgumentParser(description='Arcomics: a Bioinformatics tool \
                                                to generate Arc Diagrams from genomic data')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))
    
if __name__ == '__main__':
    main()