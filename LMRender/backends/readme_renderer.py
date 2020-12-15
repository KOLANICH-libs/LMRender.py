from itertools import product

from ..core import SF, IMapper, IRenderer

__all__ = ("RRMapper",)


class RRMapper(IMapper):
	__slots__ = ()

	LIB = "readme-renderer"
	SRC_FMTS = (SF.rst,)
	TGT_FMTS = (SF.html,)

	rrRender = None

	def render(self, rawSrc: str, fmt: SF, targetFormat: SF, renderer: IRenderer) -> str:
		return self.__class__.rrRender(rawSrc)

	@classmethod
	def ensureImported(cls) -> None:
		from readme_renderer.rst import render as rrRender

		cls.rrRender = rrRender
