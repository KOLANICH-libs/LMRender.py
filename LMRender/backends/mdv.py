from itertools import product

from ..core import SF, IMapper, IRenderer
from .markdown import MarkdownMapper

__all__ = ("MDVMapper",)


class MDVMapper(IMapper):
	__slots__ = ("mdMapper",)

	LIB = "mdv"
	SRC_FMTS = (SF.gfm,)
	TGT_FMTS = (SF.gfm_ansi,)

	AnsiPrintExtension = None
	TableExtension = None

	@classmethod
	def _render(cls, markdownStr: str) -> str:
		md = MarkdownMapper.markdown.Markdown(
			tab_length=4,
			extensions=[
				cls.AnsiPrintExtension(),
				cls.TableExtension(),
			]
			+ MarkdownMapper.extensions,
		)
		converted = md.convert(markdownStr)
		return md.ansi

	def render(self, rawSrc: str, fmt: SF, targetFormat: SF, renderer: IRenderer) -> str:
		return self.__class__._render(rawSrc)

	@classmethod
	def ensureImported(cls) -> None:
		MarkdownMapper.ensureImported()

		from mdv.markdownviewer import AnsiPrintExtension, TableExtension

		cls.AnsiPrintExtension = AnsiPrintExtension
		cls.TableExtension = TableExtension
