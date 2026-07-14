import textwrap

from beets.util.lyrics import Lyrics


class TestLyrics:
    def test_instrumental_lyrics(self):
        lyrics = Lyrics(
            "[Instrumental]", "lrclib", url="https://lrclib.net/api/1"
        )

        assert lyrics.full_text == ""
        assert lyrics.instrumental
        assert lyrics.backend == "lrclib"
        assert lyrics.url == "https://lrclib.net/api/1"
        assert lyrics.language is None
        assert lyrics.translation_language is None

    def test_from_legacy_text(self, is_importable):
        text = textwrap.dedent("""
        [00:00.00] Some synced lyrics / Quelques paroles synchronisées
        [00:00.50]
        [00:01.00] Some more synced lyrics / Quelques paroles plus synchronisées

        Source: https://lrclib.net/api/1/""")

        lyrics = Lyrics.from_legacy_text(text)

        assert lyrics.full_text == textwrap.dedent(
            """
            [00:00.00] Some synced lyrics / Quelques paroles synchronisées
            [00:00.50]
            [00:01.00] Some more synced lyrics / Quelques paroles plus synchronisées"""
        )
        assert lyrics.backend == "lrclib"
        assert lyrics.url == "https://lrclib.net/api/1/"
        langdetect_available = is_importable("langdetect")
        assert lyrics.language == ("EN" if langdetect_available else None)
        assert lyrics.translation_language == (
            "FR" if langdetect_available else None
        )
        assert not lyrics.instrumental

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
