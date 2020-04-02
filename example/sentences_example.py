from pydeeplator.deepL import DeepLTranslator
from pydeeplator.deepL import TranslateLanguageEnum, TranslateModeType

TEST_ZH_SENTENCES: str = """
今天天气很好，我和小明一起去爬山。我们在山上遇到了小红，一起快乐地写起了代码。
"""
TEST_EN_SENTENCES: str = """
Life is a journey, not the destination,
but the scenery along the should be and the mood at the view.
"""


def sentences_translate_example_zh_to_en():
    result = DeepLTranslator(
        translate_str=TEST_ZH_SENTENCES,
        target_lang=TranslateLanguageEnum.EN,
        translate_mode=TranslateModeType.SENTENCES,
    ).translate()

    print(result)


def sentences_translate_example_en_to_zh():
    result = DeepLTranslator(
        translate_str=TEST_EN_SENTENCES,
        target_lang=TranslateLanguageEnum.ZH,
        translate_mode=TranslateModeType.SENTENCES,
    ).translate()

    print(result)


def get_sentences_translate_raw_data():
    result = DeepLTranslator(
        translate_str=TEST_EN_SENTENCES,
        target_lang=TranslateLanguageEnum.ZH,
        translate_mode=TranslateModeType.SENTENCES,
        is_raw_data=True,
    ).translate()

    print(result)


if __name__ == "__main__":
    sentences_translate_example_zh_to_en()
    sentences_translate_example_en_to_zh()
    get_sentences_translate_raw_data()
