import argparse

from pathlib import Path

from collections import defaultdict


def read_text_file(path: str | Path) -> str:
	"""Odczytuje plik tekstowy w kodowaniu UTF-8."""
	return Path(path).read_text(encoding="utf-8")


def write_text_file(path: str | Path, data: str) -> None:
	"""Zapisuje tekst do pliku w kodowaniu UTF-8."""
	Path(path).write_text(data, encoding="utf-8")


def read_binary_file(path: str | Path) -> bytes:
	"""Odczytuje plik binarny."""
	return Path(path).read_bytes()


def write_binary_file(path: str | Path, data: bytes) -> None:
	"""Zapisuje dane binarne do pliku."""
	Path(path).write_bytes(data)


def count_char(input_data: str, k: int) -> defaultdict[str, int]:

    """Zlicza wystąpienia każdego znaku w danych wejściowych."""
    char_count = defaultdict(int)
    for i in range(len(input_data) - k + 1):
        substring = input_data[i:i + k]
        char_count[substring] += 1
    return char_count


def conditional_distribution(
	ngram_counts: dict[str, int],) -> dict[str, dict[str, float]]:
	#Grupuje n-gramy według pierwszego znaku i normalizuje ich częstości.
	totals: defaultdict[str, int] = defaultdict(int)

	for ngram, count in ngram_counts.items():
		if len(ngram) < 2:
			raise ValueError("Do rozkładu warunkowego n-gram musi mieć co najmniej 2 znaki.")
		totals[ngram[0]] += count

	distributions: dict[str, dict[str, float]] = {}
	for ngram, count in ngram_counts.items():
		first_char = ngram[0]
		continuation = ngram[1:]
		distributions.setdefault(first_char, {})[continuation] = count / totals[first_char]

	return distributions


def main() -> None:
	parser = argparse.ArgumentParser(description="Przetwarzanie pliku wejściowego.")
	parser.add_argument("rząd_przybliżenia", type=int)
	parser.add_argument("plik_wejściowy", type=Path)
	parser.add_argument("plik_wyjściowy", type=Path)
	parser.add_argument("rozmiar_wyjścia", type=int)
	args = parser.parse_args()

	input_data = read_text_file(args.plik_wejściowy)

    # H(X|Y) = -sigma(p1 - log2p2)
    # p1 ->prawdopodobieństwo łączne p(x, y)
    # p2 -> prawdopodobieństwo warunkowe p(x|y)

    dic1 = count_char(input_data, 1)
    dic2 = count_char(input_data, args.rząd_przybliżenia)
	conditional = conditional_distribution(dic2)
	
	#write_text_file(args.plik_wyjściowy, output_data)


if __name__ == "__main__":
	main()
