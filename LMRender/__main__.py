import argparse
import sys
from pathlib import Path

from . import DEFAULT_RENDERER, SF

p = argparse.ArgumentParser(description="Renders ReadMe in text console")
# p.add_argument("--format")
p.add_argument("file")


def main() -> None:
	args = p.parse_args()

	f = Path(args.file.strip())
	src = f.read_text()
	s = SF.fromFileName(f)

	sourceLibsNeeded = DEFAULT_RENDERER.isSourceUnavailable(s)
	if sourceLibsNeeded:
		print("Unsupported source format:", s, "you may want to install any of", sourceLibsNeeded, file=sys.stderr)
		exit(1)

	rendered = DEFAULT_RENDERER.render(src, s, SF.gfm_ansi)
	print(rendered)


if __name__ == "__main__":
	main()
