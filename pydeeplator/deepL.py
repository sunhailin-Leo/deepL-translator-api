import http
import json
import time
from typing import Dict, Sequence

import requests


# 常量
class EngineEnum:
    API_URL: str = "https://www2.deepl.com/jsonrpc"
    API_DEFAULT_HEADERS: Dict = {
        "origin": "https://www.deepl.com",
        "referer": "https://www.deepl.com/translator",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Safari/537.36",
    }

    JSON_RPC_VERSION: str = "2.0"

    Method_Translate = "LMT_handle_jobs"
    Method_Sentences = "LMT_split_into_sentences"


# 语言类型参数
class TranslateLanguageEnum:
    ZH: str = "ZH"
    EN: str = "EN"
    DE: str = "DE"
    FR: str = "FR"
    ES: str = "ES"
    PT: str = "PT"
    IT: str = "IT"
    NL: str = "NL"
    PL: str = "PL"
    RU: str = "RU"
    JA: str = "JA"

    LanguageCodeToNameMap: Dict = {
        "ZH": "中文",
        "EN": "英语",
        "DE": "德语",
        "FR": "法语",
        "ES": "西班牙语",
        "PT": "葡萄牙语",
        "IT": "意大利语",
        "NL": "荷兰语",
        "PL": "波兰语",
        "RU": "俄语",
        "JA": "日语",
    }

    LanguageNameToCodeMap: Dict = {
        "中文": "ZH",
        "英语": "EN",
        "德语": "DE",
        "法语": "FR",
        "西班牙语": "ES",
        "葡萄牙语": "PT",
        "意大利语": "IT",
        "荷兰语": "NL",
        "波兰语": "PL",
        "俄语": "RU",
        "日语": "JA",
    }

    LanguageList: Sequence[str] = [
        "ZH",
        "EN",
        "DE",
        "FR",
        "ES",
        "PT",
        "IT",
        "NL",
        "PL",
        "RU",
        "JA",
    ]


# 模式参数
class TranslateModeType:
    AUTO: str = "auto"
    WORD: str = "word"
    SENTENCES: str = "sentences"


class _DeepLTranslatorEngine:
    def __init__(
        self,
        translate_str: str,
        target_lang: str,
        source_lang: str = "auto",
        translate_mode: str = TranslateModeType.AUTO,
        is_raw_data: bool = False,
    ):
        self._translate_str = translate_str

        self._target_lang = target_lang
        if self._target_lang != "auto" and \
                self._target_lang not in TranslateLanguageEnum.LanguageList:
            raise ValueError("target_lang (目标语言) 参数错误!")

        self._source_lang = source_lang
        if self._source_lang != "auto" and \
                self._source_lang not in TranslateLanguageEnum.LanguageList:
            raise ValueError("source_lang (源语言) 参数错误!")

        self._translate_mode = translate_mode
        self._is_raw_data = is_raw_data

    def translate(self) -> Dict:
        if self._translate_mode == TranslateModeType.AUTO \
                or self._translate_mode == TranslateModeType.SENTENCES:
            return self._translate_sentences()
        elif self._translate_mode == TranslateModeType.WORD:
            return self._translate_word()
        else:
            raise ValueError("translate_mode (翻译模式) 参数错误!")

    def _translate_word(self) -> Dict:
        job_dict_list = [
            {
                "kind": "default",
                "raw_en_sentence": word,
                "raw_en_context_before": [],
                "raw_en_context_after": [],
                "preferred_num_beams": 1,
            }
            for word in [self._translate_str]
        ]
        return self._prepare_call_translate_api(
            job_dict_list=job_dict_list, lang="auto"
        )

    def _translate_sentences(self) -> Dict:
        sentences_data: Dict = {
            "jsonrpc": EngineEnum.JSON_RPC_VERSION,
            "method": EngineEnum.Method_Sentences,
            "params": {
                "texts": [self._translate_str],
                "lang": {"lang_user_selected": self._translate_mode},
            },
        }
        split_result = self._core_request(request_data=sentences_data)
        lang = split_result["result"]["lang"]
        texts = split_result["result"]["splitted_texts"][0]

        job_dict_list = [
            {
                "kind": "default",
                "raw_en_sentence": sentence,
                "raw_en_context_before": [],
                "raw_en_context_after": [sentence],
                "preferred_num_beams": 1,
            }
            for sentence in texts
        ]
        return self._prepare_call_translate_api(job_dict_list=job_dict_list, lang=lang)

    def _prepare_call_translate_api(self, job_dict_list: Sequence[Dict], lang: str):
        translate_data: Dict = {
            "jsonrpc": EngineEnum.JSON_RPC_VERSION,
            "method": EngineEnum.Method_Translate,
            "params": {
                "jobs": job_dict_list,
                "lang": {
                    "source_lang_computed": lang,
                    "target_lang": self._target_lang,
                },
                "priority": 1,
                "commonJobParams": {},
                "timestamp": int(time.time() * 1000),
            },
        }
        translate_result = self._core_request(request_data=translate_data)
        return self._package_response_data(translate_result=translate_result)

    def _package_response_data(self, translate_result: Dict):
        if self._is_raw_data:
            return translate_result
        else:
            translate_result_list = [
                result["beams"][0]["postprocessed_sentence"]
                for result in translate_result["result"]["translations"]
            ]
            return {"result": "".join(translate_result_list)}

    @staticmethod
    def _core_request(request_data: Dict) -> Dict:
        resp = requests.post(
            url=EngineEnum.API_URL,
            headers=EngineEnum.API_DEFAULT_HEADERS,
            json=request_data,
        )
        if resp.status_code != http.HTTPStatus.OK:
            raise Exception("API 不可用!")
        return resp.json()


DeepLTranslator = _DeepLTranslatorEngine
