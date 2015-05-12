# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2015 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for position_caret.js."""

import pytest

from PyQt5.QtCore import Qt
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebPage


@pytest.fixture(autouse=True)
def enable_caret_browsing():
    """Fixture to enable caret browsing globally."""
    QWebSettings.globalSettings().setAttribute(
        QWebSettings.CaretBrowsingEnabled, True)


class CaretTester:

    """Helper class (for the caret_tester fixture) for asserts.

    Attributes:
        js: The js_tester fixture.
    """

    def __init__(self, js_tester):
        self.js = js_tester

    def check(self):
        """Check whether the caret is before the MARKER text."""
        self.js.run_file('position_caret.js')
        self.js.webview.triggerPageAction(QWebPage.SelectNextWord)
        assert self.js.webview.selectedText() == "MARKER"

    def check_scrolled(self):
        """Check if the page is scrolled down."""
        frame = self.js.webview.page().mainFrame()
        minimum = frame.scrollBarMinimum(Qt.Vertical)
        value = frame.scrollBarValue(Qt.Vertical)
        assert value > minimum


@pytest.fixture
def caret_tester(js_tester):
    """Helper fixture to test caret browsing positions."""
    return CaretTester(js_tester)


def test_simple(caret_tester):
    """Test with a simple (one-line) HTML text."""
    caret_tester.js.load('position_caret/simple.html')
    caret_tester.check()


def test_scrolled_down(caret_tester):
    """Test with multiple text blocks with the viewport scrolled down."""
    caret_tester.js.load('position_caret/scrolled_down.html')
    caret_tester.js.scroll_anchor('anchor')
    caret_tester.check_scrolled()
    caret_tester.check()
