from pydeeplator.deepL import DeepLTranslator
from pydeeplator.deepL import TranslateLanguageEnum, TranslateModeType


def word_translate_example_zh_to_en():
    result = DeepLTranslator(
        translate_str="水印",
        target_lang=TranslateLanguageEnum.EN,
        translate_mode=TranslateModeType.WORD,
    ).translate()

    # result: {'result': 'watermark'}
    print(result)


def word_translate_example_zh_to_ja():
    result = DeepLTranslator(
        translate_str="水印",
        target_lang=TranslateLanguageEnum.JA,
        translate_mode=TranslateModeType.WORD,
    ).translate()

    # {'result': '透かし'}
    print(result)


def word_translate_example_ja_to_en():
    result = DeepLTranslator(
        translate_str="透かし",
        source_lang=TranslateLanguageEnum.JA,
        target_lang=TranslateLanguageEnum.EN,
        translate_mode=TranslateModeType.WORD,
    ).translate()

    # {'result': 'watermark'}
    print(result)


def get_translate_raw_data_example():
    result = DeepLTranslator(
        translate_str="透かし",
        source_lang=TranslateLanguageEnum.JA,
        target_lang=TranslateLanguageEnum.EN,
        translate_mode=TranslateModeType.WORD,
        is_raw_data=True,
    ).translate()

    # raw data
    print(result)


if __name__ == "__main__":
    word_translate_example_zh_to_en()
    word_translate_example_zh_to_ja()
    word_translate_example_ja_to_en()
    get_translate_raw_data_example()
