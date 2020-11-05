# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from ctypes import c_bool, c_char, c_char_p, c_double, c_int, c_uint, POINTER, Structure, byref, c_ulong
import typing


class DocExtractor(NLPIRBase):
    """
    A dynamic link library native class for Doc entity Extract
    """

    @property
    def dll_name(self) -> str:
        return "DocExtractor"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
        Call **Doc_Entity_Extract_Init**

        :param str data_path:
        :param int encode:
        :param str license_code:
        :return: 1 success 0 fail
        """
        return self.get_func('DocExtractor_Init', [c_char_p, c_int, c_char_p], c_int)(data_path, encode, license_code)

    def exit_lib(self) -> bool:
        """
        Call **DocExtractor_Exit**

        :return: exit success or not
        """
        return self.get_func('DocExtractor_Exit',[None] ,restype=c_bool)()

    @NLPIRBase.byte_str_transform
    def get_entity(self, line: str, max_key_limit: int = 50, weight_out: bool = False) -> str:
        """
        Call **DocExtractor_GetEntityWords**

        Description: Extract entity from sLine

        :param line: the input paragraph
        :param max_key_limit: maximum of entity words, up to 50
        :param weight_out: whether the entityword weight output
        :return: "卢梭/人名/23.14 日内瓦共和国/地名/26.32" 分别表示 实体词/实体词属性/权重
        """
        return self.get_func('DocExtractor_GetEntityWords', [c_char_p, c_int, c_bool], c_char_p)(
            line,
            max_key_limit,
            weight_out
        )

    @NLPIRBase.byte_str_transform
    def import_user_dict(self, filename: str, overwrite: bool = False):
        """
        Call **DocExtractor_ImportUserDict**

        Import entityword user defined dictionary

        :param filename: Text filename for user dictionary, each line for a imported entityword
        :param overwrite:
        :return: The number of lexical entry imported successfully
        """
        return self.get_func('DocExtractor_ImportUserDict', [c_char_p, c_bool], c_uint)(filename, overwrite)

    @NLPIRBase.byte_str_transform
    def add_user_word(self, word: str) -> int:
        """
        Call **DocExtractor_AddUserWord**

        add a word to the user dictionary ,example::

            北京西 entity

        需要作为实体词的，标引前缀必须为entity

        :param word: 加入到临时用户词典
        实体词属性与实体词，用空格分割
        :return: 1,true ; 0,false
        """
        return self.get_func('KeyExtract_AddUserWord', [c_char_p], c_int)(word)

    @NLPIRBase.byte_str_transform
    def clean_user_word(self) -> int:
        """
        Call **DocExtractor_CleanUserWord**

        Clean all temporary added user words

        :return: 1,true ; 0,false
        """
        return self.get_func('DocExtractor_CleanUserWord', None, c_int)()

    @NLPIRBase.byte_str_transform
    def save_the_usr_dict(self) -> int:
        """
        Call **DocExtractor_SaveTheUsrDic**

        Save dictionary to file

        :return: 1,true; 2,false
        """
        return self.get_func('DocExtractor_SaveTheUsrDic', None, c_int)()

    @NLPIRBase.byte_str_transform
    def del_usr_word(self, word: str) -> int:
        """
        Call **DocExtractor_DelUsrWord**

        delete a word from the user dictionary

        :param word:
        :return: -1, the word not exist in the user dictionary; else, the handle of the word deleted

        """
        return self.get_func('DocExtractor_DelUsrWord', [c_char_p], c_int)(word)

    @NLPIRBase.byte_str_transform
    def import_entity_blacklist(self, filename: str, pos_blacklist: typing.Optional[str] = None) -> int:
        """
        Call **KeyExtract_ImportKeyBlackList**

        Import keyword black list

        import_blacklist will ass word to KeyBlackList.pdat remove the words form it need to backup it after use this function.
        this list of word will not affect the key word extract and segmentation


        :param filename: Text filename for user defined blacklist dictionary, each line for a stop keyword
        :param pos_blacklist: 停用的词性列表，即列为该词性列表访问的词不纳入实体词范围,如设置为#nr#ns#表示nr,ns不作为实体词
        :return: The number of lexical entry imported successfully
        """
        return self.get_func('DocExtractor_ImportentityBlackList', [c_char_p, c_char_p], c_uint)(filename, pos_blacklist)

    """
    /*********************************************************************
    *
    以下函数为2013版本专门针对实体词批量发现的过程，一般建议脱机实现，不宜在线处理
    *********************************************************************/
    """

    @NLPIRBase.byte_str_transform
    def batch_start(self) -> int:
        """
        Call **DocEntityExtract_Batch_Start**

        启动实体词识别

        :return: true:success, false:fail
        """
        return self.get_func('DocExtractor_Batch_Start', None, c_int)()

    @NLPIRBase.byte_str_transform
    def batch_add_file(self, filename) -> int:
        """
        Call **DocEntityExtract_Batch_AddFile**

        往实体词识别系统中添加待识别实体词的文本文件,需要在运行DocEntityExtract_Batch_Start()之后，才有效

        :param filename: 文件名
        :return: bool, true:success, false:fail
        """
        return self.get_func('DocExtractor_Batch_AddFile', [c_char_p], c_ulong)(filename)

    @NLPIRBase.byte_str_transform
    def batch_addmen(self, txt: str) -> bool:
        """
        Call **DocEntityExtract_Batch_AddMem**
        往实体词识别系统中添加一段待识别实体词的内存,需要在运行DocEntityExtract_Batch_Start()之后，才有效

        :param txt: string
        :return: true:success, false:fail
        """
        return self.get_func('DocExtractor_Batch_AddMem', [c_char_p], c_bool)(txt)

    @NLPIRBase.byte_str_transform
    def batch_complete(self) -> int:
        """
        Call **DocExtractor_Batch_Complete**

        实体词识别添加内容结束,需要在运行DocEntityExtract_Batch_Start()之后，才有效

        :return: true:success, false:fail
        """
        return self.get_func('DocExtractor_Batch_Complete', None, c_int)()

    @NLPIRBase.byte_str_transform
    def batch_getresult(self, weight_out: bool = False) -> str:
        """
        Call **DocEntityExtract_Batch_GetResult**

        获取关键词识别的结果, 需要在运行DocEntityExtract_Batch_Complete()之后，才有效

        :param weight_out: 是否需要输出每个关键词的权重参数
        :return: 输出格式为:【关键词属性】 【实体词】 ...
        """
        return self.get_func('DocExtractor_Batch_GetResult', None, str)()

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        """
        Call **DocExtractor_GetLastErrorMsg**

        :return: error message
        """
        return self.get_func("DocExtractor_GetLastErrorMsg", None, c_char_p)()
