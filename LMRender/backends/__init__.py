from ..core import Renderer
from .markdown import MarkdownMapper
from .markdownify import MarkdownifyMapper
from .mdv import MDVMapper
from .pandoc import PandocMapper
from .readme_renderer import RRMapper

__all__ = ("initDefaultRenderer",)

PANDOC_COST = 3


def initDefaultRenderer() -> Renderer:
	ctors = [
		MarkdownifyMapper,
		MarkdownMapper,
		RRMapper,
		MDVMapper,
		(PandocMapper, PANDOC_COST),
	]
	return Renderer.fromCtors(ctors)
