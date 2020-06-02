import argparse
import math
import sys

try:
    # Python 3.8
    from math import comb
except ImportError:
    try:
        # fallback to scipy
        from scipy.special import comb
    except ImportError:
        # naive implementation
        def comb(n, k):
            if n < 0 or k < 0:
                raise ValueError("arguments should be positive integer")
            if n < k:
                return 0
            if n == k:
                return 1
            return math.factorial(n) // math.factorial(k) // math.factorial(n - k)


try:
    # Python 3.5
    from math import isclose
except ImportError:
    # naive implementation
    def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
        return math.abs(a - b) <= max(rel_tol * max(math.abs(a), math.abs(b)), abs_tol)


def expected_maximum_performance(values, biased=False):
    """ Estimate the expected maximum performance as a function of the number of trials

    Methods from "Showing Your Work Doesn't Always Work" (Tang, et al, ACL 2020)
    <https://arxiv.org/abs/2004.13705>, which is based on "Show Your Work: Improved
    Reporting of Experimental Results" (Dodge, et al, EMNLP 2019)
    <https://arxiv.org/abs/1909.03004>.

    Arguments:
        values (List[Number]): the performance measurements from multiple experiments
        biased (bool): if True, use the biased version in (Dodge, et al, 2019); or use
                       the unbiased version in (Tang, et al, 2020)
    Return:
        List[Number]: the expected maximum performance for the number of trials
    """
    values = sorted(values)
    sample_size = len(values)

    def calculate_for_n(n):
        if biased:
            denominator = sample_size ** n
            return sum(
                value * ((index + 1) ** n - index ** n) / denominator
                for index, value in enumerate(values)
            )
        denominator = comb(sample_size, n)
        return sum(
            value * comb(index, n - 1) / denominator
            for index, value in enumerate(values)
        )

    expected_maximums = [calculate_for_n(n) for n in range(1, sample_size + 1)]

    # basic checks
    # assert isclose(expected_maximums[0], sum(values) / sample_size)
    # assert all(maximum <= values[-1] for maximum in expected_maximums)

    return expected_maximums


def _format_numbers(numbers):
    return ["{:.6f}".format(n) for n in numbers]


def main():
    parser = argparse.ArgumentParser(
        description="Script to caculate the expected validation performance proposed in "
        "(Dodge, et al, 2019)",
        epilog="If neither file or numbers are given, interactive mode will be used. "
        "Enter a number on each line. Empty line to end. The numbers option is preferred "
        "over the file option",
    )
    parser.add_argument(
        "-f",
        "--file",
        metavar="FILE",
        type=str,
        default=None,
        help="Read values from file (one value per line)",
    )
    parser.add_argument(
        "-n",
        "--numbers",
        metavar="NUM",
        type=float,
        nargs="*",
        default=None,
        help="Values",
    )
    parser.add_argument(
        "-b",
        "--biased",
        action="store_true",
        default=False,
        help="Use the original biased version",
    )
    parser.add_argument(
        "-p",
        "--print",
        action="store_true",
        default=False,
        help="Print the results, a number per line",
    )

    args = parser.parse_args()

    numbers = args.numbers
    if not numbers and args.file:
        try:
            numbers = []
            with open(args.file, "r", encoding="utf8") as f:
                for line in f:
                    try:
                        numbers.append(float(line.strip()))
                    except ValueError:
                        print(
                            'Line format not recoginzed: "'
                            + line.strip()
                            + '", skipped',
                            file=sys.stderr,
                        )
                if not numbers:
                    print(
                        "No numbers are read, enter interactive mode", file=sys.stderr
                    )
        except FileNotFoundError:
            print("File not found, enter interactive mode", file=sys.stderr)

    if not numbers:
        numbers = []
        while True:
            line = input("> ").strip()
            if not line:
                break
            try:
                numbers.append(float(line.strip()))
            except ValueError:
                print(
                    'Line format not recoginzed: "' + line.strip() + '", skipped',
                    file=sys.stderr,
                )

    if not numbers:
        print("No numbers given, end script.", file=sys.stderr)
        return

    print("Numbers:", _format_numbers(numbers))

    results = _format_numbers(expected_maximum_performance(numbers, args.biased))

    if args.print:
        print("Expected Maximum Performance" + (" (biased):" if args.biased else ":"))
        for n in results:
            print(n)
    else:
        print(
            "Expected Maximum Performance" + (" (biased):" if args.biased else ":"),
            results,
        ),


if __name__ == "__main__":
    main()
