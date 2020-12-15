from itertools import product

from ..core import SF, IMapper, IRenderer

__all__ = ("MarkdownifyMapper",)


class MarkdownifyMapper(IMapper):
	__slots__ = ()

	LIB = "markdownify"
	SRC_FMTS = (SF.html,)
	TGT_FMTS = (SF.gfm,)

	markdownify = None

	def render(self, rawSrc: str, fmt: SF, targetFormat: SF, renderer: IRenderer) -> str:
		return self.__class__.markdownify.markdownify(rawSrc)

	@classmethod
	def ensureImported(cls) -> None:
		import markdownify

		cls.markdownify = markdownify
