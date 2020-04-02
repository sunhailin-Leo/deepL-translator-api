from nose.tools import assert_equal
from pydeeplator.deepL import DeepLTranslator, TranslateModeType, TranslateLanguageEnum

TEST_ZH_SENTENCES: str = """
今天天气很好，我和小明一起去爬山。我们在山上遇到了小红，一起快乐地写起了代码。
"""


def test_translate_word():
    result = DeepLTranslator(
        translate_str="水印",
        target_lang=TranslateLanguageEnum.EN,
        translate_mode=TranslateModeType.WORD,
    ).translate()

    assert_equal(result, {"result": "watermark"})


def test_translate_sentences():
    result = DeepLTranslator(
        translate_str=TEST_ZH_SENTENCES,
        target_lang=TranslateLanguageEnum.EN,
        translate_mode=TranslateModeType.SENTENCES,
    ).translate()

    assert_equal(
        result,
        {
            "result": "It was a beautiful day and I went hiking with Xiao Ming."
            "We met Little Red in the mountains and happily wrote code together."
        },
    )
