# stdlib
import ast
import io
import itertools
import re
import types
from email.headerregistry import Address
from typing import Any, List

# 3rd party
import pytest
from coincidence.selectors import not_pypy, only_pypy
from domdf_python_tools.typing import (
		ClassMethodDescriptorType,
		MethodDescriptorType,
		MethodWrapperType,
		WrapperDescriptorType
		)
from sphinx.errors import ExtensionError
from typing_extensions import Protocol

# this package
from sphinx_toolbox import __version__
from sphinx_toolbox.more_autodoc import typehints
from sphinx_toolbox.testing import Sphinx, run_setup


@pytest.mark.parametrize(
		"annotation, expected",
		[
				pytest.param(None, ":py:obj:`None`", id="None"),
				pytest.param(type(None), ":py:obj:`None`", id="NoneType"),
				pytest.param(Ellipsis, "...", id="Ellipsis"),
				pytest.param(..., "...", id="..."),
				pytest.param(itertools.cycle, ":func:`itertools.cycle`", id="itertools.cycle"),
				pytest.param(
						types.GetSetDescriptorType,
						":py:data:`types.GetSetDescriptorType`",
						id="types.GetSetDescriptorType"
						),
				pytest.param(
						types.MemberDescriptorType,
						":py:data:`types.MemberDescriptorType`",
						id="types.MemberDescriptorType"
						),
				pytest.param(
						ClassMethodDescriptorType,
						":py:data:`types.ClassMethodDescriptorType`",
						id="types.ClassMethodDescriptorType"
						),
				pytest.param(
						MethodDescriptorType,
						":py:data:`types.MethodDescriptorType`",
						id="types.MethodDescriptorType"
						),
				pytest.param(
						MethodWrapperType,
						":py:data:`types.MethodWrapperType`",
						id="types.MethodWrapperType",
						marks=not_pypy("PyPy reuses some types"),
						),
				pytest.param(
						MethodWrapperType,
						":py:data:`types.MethodType`",
						id="types.MethodWrapperType",
						marks=only_pypy("PyPy reuses some types"),
						),
				pytest.param(
						WrapperDescriptorType,
						":py:data:`types.WrapperDescriptorType`",
						id="types.WrapperDescriptorType",
						marks=not_pypy("PyPy reuses some types")
						),
				pytest.param(
						WrapperDescriptorType,
						":py:data:`types.MethodDescriptorType`",
						id="types.WrapperDescriptorType",
						marks=only_pypy("PyPy reuses some types")
						),
				pytest.param(
						types.BuiltinFunctionType,
						":py:data:`types.BuiltinFunctionType`",
						id="types.BuiltinFunctionType"
						),
				pytest.param(
						types.MethodType,
						":py:data:`types.MethodType`",
						id="types.MethodType",
						),
				pytest.param(
						types.MappingProxyType, ":py:class:`types.MappingProxyType`", id="types.MappingProxyType"
						),
				pytest.param(types.ModuleType, ":py:class:`types.ModuleType`", id="types.ModuleType"),
				pytest.param(type(re.compile('')), ":py:class:`typing.Pattern`", id="regex"),
				pytest.param(List, ":py:class:`typing.List`", id="typing.List"),
				pytest.param(Protocol, ":py:class:`typing.Protocol`", id="typing_extensions.Protocol"),
				pytest.param(
						Address, ":py:class:`email.headerregistry.Address`", id="email.headerregistry.Address"
						),
				pytest.param(io.StringIO, ":py:class:`io.StringIO`", id="io.StringIO"),
				pytest.param(ast.AST, ":py:class:`ast.AST`", id="ast.AST"),
				]
		)
def test_format_annotation(annotation: Any, expected: str):
	assert typehints.format_annotation(annotation, True) == expected


def test_setup():
	try:
		Sphinx.extensions = []  # type: ignore

		setup_ret, directives, roles, additional_nodes, app = run_setup(typehints.setup)

		assert setup_ret == {"parallel_read_safe": True, "version": __version__}

		assert app.config.values["hide_none_rtype"] == (False, "env", [bool])

		assert directives == {}
		assert roles == {}
		assert additional_nodes == set()

	finally:
		del Sphinx.extensions  # type: ignore


def test_setup_wrong_order():
	try:
		Sphinx.extensions = ["sphinx_autodoc_typehints"]  # type: ignore

		with pytest.raises(
				ExtensionError,
				match="'sphinx_toolbox.more_autodoc.typehints' "
				"must be loaded before 'sphinx_autodoc_typehints'.",
				):

			run_setup(typehints.setup)

	finally:
		del Sphinx.extensions  # type: ignore
