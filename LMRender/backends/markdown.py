from itertools import product

from ..core import SF, IMapper, IRenderer

__all__ = ("MarkdownMapper",)


class MarkdownMapper(IMapper):
	__slots__ = ()

	LIB = "markdown"
	SRC_FMTS = (SF.gfm,)
	TGT_FMTS = (SF.html,)

	markdown = None
	extensions = ()

	@classmethod
	def _render(cls, markdownStr: str) -> str:
		md = cls.markdown.Markdown(
			tab_length=4,
			extensions=cls.extensions,
		)
		converted = md.convert(markdownStr)
		return converted

	def render(self, rawSrc: str, fmt: SF, targetFormat: SF, renderer: IRenderer) -> str:
		if fmt != self.__class__.SRC_FMTS[0]:
			rawSrc = renderer.convert(rawSrc, fmt, self.__class__.SRC_FMTS[0])

		return _render(rawSrc)

	@classmethod
	def ensureImported(cls) -> None:
		import markdown
		from markdown.extensions.fenced_code import FencedCodeExtension

		cls.markdown = markdown
		cls.extensions = [
			FencedCodeExtension(),
		]
