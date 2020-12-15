import typing
from itertools import product

from ..core import SF, IMapper, IRenderer

__all__ = ("PandocMapper",)


class PandocMapper(IMapper):
	__slots__ = ()

	LIB = "pypandoc"
	SRC_FMTS = (SF.gfm, SF.html, SF.mediawiki, SF.ipynb)
	TGT_FMTS = SRC_FMTS + (SF.rst,)

	pypandoc = None

	@classmethod
	def pandocFormatsIntoSF(cls, formatsList: typing.List[str]) -> typing.Iterable[SF]:
		found = []

		for el in formatsList:
			try:
				res = SF[el]
			except KeyError:
				pass
			else:
				if res:
					found.append(res)
		return tuple(set(found))

	@classmethod
	def findSFs(cls):
		return tuple(map(cls.pandocFormatsIntoSF, cls.pypandoc.get_pandoc_formats()))

	@classmethod
	def generateMatrix(cls, renderer: IRenderer) -> product:
		fr, to = cls.findSFs()
		return product(fr, to)

	def render(self, rawSrc: str, fmt: SF, targetFormat: SF, renderer: IRenderer) -> str:
		return self.__class__.pypandoc.convert_text(
			rawSrc,
			targetFormat.value + "+smart",
			fmt.value,
			extra_args=("--indent=none",),
		)

	@classmethod
	def ensureImported(cls) -> None:
		import pypandoc

		cls.pypandoc = pypandoc
