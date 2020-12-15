import typing
from collections import defaultdict
from enum import Enum
from itertools import product
from os import geteuid
from pathlib import Path, PurePath

__all__ = ("SupportedFormat", "SF", "IMapper", "IRenderer", "MapperAlreadyPresentError", "Renderer")


class SupportedFormat(Enum):
	gfm_ansi = "gfm_ansi"
	gfm = commonmark = md = markdown = "gfm"
	asciidoc = adoc = asciidoctor = "asciidoctor"
	html = htm = xhtml = "html"
	mediawiki = "mediawiki"
	rst = "rst"
	ipynb = "ipynb"
	text = txt = plain = "plain"
	rtf = "rtf"

	@classmethod
	def fromFileName(cls, fileName: PurePath) -> "SupportedFormat":
		suff = fileName.suffix.lower()

		if suff and suff[0] == ".":
			suff = suff[1:]
		else:
			return None

		return cls[suff]


SF = SupportedFormat


class IRenderer:
	__slots__ = ()

	def isSourceUnavailable(self, fmt: SF) -> typing.Iterable[str]:
		raise NotImplementedError

	def render(self, rawSrc: str, fmt: SF, targetFormat: SF) -> str:
		raise NotImplementedError


class IMapper:
	__slots__ = ("cost",)

	LIB = None  # type: str

	SRC_FMTS = None  # type: typing.Tuple[SF]
	TGT_FMTS = None  # type: typing.Tuple[SF]

	DEFAULT_COST = 1

	def __init__(self, cost: typing.Optional[int] = None) -> None:
		if cost is None:
			cost = self.__class__.DEFAULT_COST

		self.cost = cost

	@classmethod
	def generateMatrix(cls, renderer: IRenderer) -> product:
		return product(cls.SRC_FMTS, cls.TGT_FMTS)

	def ensureImported(self) -> str:
		raise NotImplementedError

	def render(self, rawSrc: str, fmt: SF, targetFormat: SF, renderer: IRenderer) -> str:
		raise NotImplementedError


class MapperAlreadyPresentError(RuntimeError):
	pass


class Renderer(IRenderer):
	__slots__ = ("mappers",)

	def __init__(self, backends: typing.List[IMapper]) -> None:
		self.mappers = None  # type: typing.Dict[SF, typing.Dict[SF, typing.Union[IMapper, (IMapper, SF)]]]
		self.initializeBackends(backends)

	@classmethod
	def fromCtors(cls, ctors: typing.List[typing.Union[typing.Type[IMapper], typing.Tuple[typing.Type[IMapper], int]]]) -> "Renderer":
		backends = []
		for ctor in ctors:
			if isinstance(ctor, tuple):
				ctor, cost = ctor
			else:
				cost = ctor.DEFAULT_COST

			try:
				ctor.ensureImported()
			except ImportError:
				pass
			else:
				backends.append(ctor(cost))
		return cls(backends)

	def initializeBackends(self, backends: typing.List[IMapper]) -> None:
		self.mappers = {}
		self.appendBackends(backends)

	def appendBackends(self, backends: typing.List[IMapper]) -> None:
		self.mappers = {}  # type: typing.Dict[SF, typing.Dict[SF, typing.Union[IMapper, (IMapper, SF)]]]
		for b in backends:
			self._injectMatrix(b)
		self._floydWarshall()

	def buildAdjAndPathMat(self, sfs: typing.List[SF]) -> typing.Tuple[typing.List[typing.List[int]], int]:
		adj = [[] for k in sfs]

		maX = len(sfs) + 1

		for i, a in enumerate(sfs):
			ar = adj[i]
			for j, b in enumerate(sfs):
				el = self.mappers.get(a, {}).get(b, None)
				if el is not None:
					v = el.cost
				else:
					v = maX
				ar.append(v)

		return adj, maX

	def _floydWarshall(self) -> None:
		sfs = list(SF)

		adj, maX = self.buildAdjAndPathMat(sfs)

		for k, c in enumerate(sfs):
			for i, a in enumerate(sfs):
				for j, b in enumerate(sfs):
					if i != j and j != k and i != k:
						c1 = adj[i][k]
						c2 = adj[k][j]
						c3 = adj[i][j]
						comb = c1 + c2

						if c3 > comb:
							adj[i][j] = comb

							pr = self.mappers.get(a, None)
							if pr is None:
								self.mappers[a] = pr = {}

							pr[b] = (self.mappers[a][c], c)

	def _injectMappers(self, f: SF, t: SF, mapper: IMapper, silent: bool = False) -> None:
		fDic = self.mappers.get(f, None)
		if fDic is None:
			self.mappers[f] = fDic = {}

		if t not in fDic:
			self.mappers[f][t] = mapper
		else:
			if not silent:
				raise MapperAlreadyPresentError("Mapper already present", f, t)

	def _injectMatrix(self, mapper: IMapper, matrix=None) -> None:
		if matrix is None:
			matrix = mapper.__class__.generateMatrix(self)

		for f, t in matrix:
			self._injectMappers(f, t, mapper, silent=True)

	def _getConvertibleTo(self, needed: SF):
		sources = []
		for s, ts in self.mappers.items():
			if needed in set(ts):
				sources.append(s)
		return sources

	def isSourceUnavailable(self, fmt: SF) -> typing.Iterable[str]:
		"""Returns an iterable of libs to install to make the source format available."""

		if fmt in self.mappers:
			return ()
		else:
			return self.sourceLibs[fmt]

	def render(self, rawSrc: str, fmt: SF, targetFormat: SF) -> str:
		if fmt == targetFormat:
			return src

		res = rawSrc
		while fmt != targetFormat:
			mapperSpec = self.mappers[fmt][targetFormat]

			if isinstance(mapperSpec, tuple):
				m, intermediateFormat = mapperSpec
			else:
				m = mapperSpec
				intermediateFormat = targetFormat

			res = m.render(res, fmt, intermediateFormat, self)
			fmt = intermediateFormat

		return res
