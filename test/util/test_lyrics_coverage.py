"""Testes de cobertura para caminhos de beets.util.lyrics.Lyrics (#L)."""

from beets.util.lyrics import Lyrics


class TestLyricsCoverage:
    def test_from_legacy_text_without_source(self):
        """Sem a linha 'Source:', nao ha backend nem url."""
        lyrics = Lyrics.from_legacy_text("just some lyrics")

        assert lyrics.text == "just some lyrics"
        assert lyrics.url is None
        assert lyrics.backend is None

    def test_from_legacy_text_unknown_backend_is_google(self):
        """URL de origem fora da lista conhecida e classificada como 'google'."""
        lyrics = Lyrics.from_legacy_text(
            "body\n\nSource: https://www.example.com/song"
        )

        assert lyrics.url == "https://www.example.com/song"
        assert lyrics.backend == "google"

    def test_original_text_strips_translations(self):
        lyrics = Lyrics("linha original / translated line")

        assert lyrics.original_text == "linha original"

    def test_timestamps_and_text_lines(self):
        lyrics = Lyrics("[00:01.00] first\nno ts line")

        assert lyrics.timestamps == ["[00:01.00]", ""]
        assert lyrics.text_lines == ["first", "no ts line"]

    def test_full_text_merges_translations(self):
        lyrics = Lyrics("hello\nworld")
        lyrics.translations = ["ola", "mundo"]

        assert lyrics.translated is False
        assert lyrics.full_text == "hello / ola\nworld / mundo"

    def test_full_text_without_translations_returns_text(self):
        lyrics = Lyrics("hello\nworld")

        assert lyrics.full_text == "hello\nworld"
