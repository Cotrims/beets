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

    def test_sylt_centiseconds(self):
        """LRC com fracao de 2 digitos e lida como centesimos de segundo."""
        lyrics = Lyrics("[00:12.34] hello\n[01:00.00] world")

        assert lyrics.sylt == [("hello", 12340), ("world", 60000)]

    def test_sylt_milliseconds(self):
        """LRC com fracao de 3 digitos e lida como milesimos de segundo."""
        lyrics = Lyrics("[00:12.345] hello\n[01:02.007] world")

        assert lyrics.sylt == [("hello", 12345), ("world", 62007)]

    def test_sylt_skips_unsynced_lines(self):
        """Linhas sem timestamp nao entram no frame SYLT."""
        lyrics = Lyrics("[00:01.00] a\nno timestamp\n[00:02.500] b")

        assert lyrics.sylt == [("a", 1000), ("b", 2500)]
        assert lyrics.synced is True

    def test_not_synced_without_timestamps(self):
        lyrics = Lyrics("plain line\nanother line")

        assert lyrics.sylt == []
        assert lyrics.synced is False
