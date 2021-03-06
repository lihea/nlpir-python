# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from ctypes import c_bool, c_char, c_char_p, c_double, c_int, c_uint, POINTER, Structure, byref, c_ulong
import typing


class KeyExtract(NLPIRBase):
    """
    A dynamic link library native class for Key Words Extract
    """

    @property
    def dll_name(self) -> str:
        return "KeyExtract"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
        Call **KeyExtract_Init**

        :param str data_path:
        :param int encode:
        :param str license_code:
        :return: 1 success 0 fail
        """
        return self.get_func('KeyExtract_Init', [c_char_p, c_int, c_char_p], c_int)(data_path, encode, license_code)

    def exit_lib(self) -> bool:
        """
        Call **KeyExtract_Exit**

        :return: exit success or not
        """
        return self.get_func('KeyExtract_Exit', restype=c_bool)()

    @NLPIRBase.byte_str_transform
    def get_keywords(self, line: str, max_key_limit: int = 50, weight_out: bool = False) -> str:
        """
        Call **KeyExtract_GetKeyWords**

        Description: Extract keyword from sLine

        :param line: the input paragraph
        :param max_key_limit: maximum of key words, up to 50
        :param weight_out: whether the keyword weight output
        :return: "科学发展观/n/23.80 宏观经济/n/12.20" with weight 分别表示 关键词/关键词词性/权重 or JSON
        """
        return self.get_func('KeyExtract_GetKeyWords', [c_char_p, c_int, c_bool], c_char_p)(
            line,
            max_key_limit,
            weight_out
        )

    @NLPIRBase.byte_str_transform
    def import_user_dict(self, filename: str, overwrite: bool = False):
        """
        Call **KeyExtract_ImportUserDict**

        Import keyword user defined dictionary

        :param filename: Text filename for user dictionary, each line for a imported keyword
        :param overwrite:
        :return: The number of lexical entry imported successfully
        """
        return self.get_func('KeyExtract_ImportUserDict', [c_char_p, c_bool], c_uint)(filename, overwrite)

    @NLPIRBase.byte_str_transform
    def add_user_word(self, word: str) -> int:
        """
        Call **KeyExtract_AddUserWord**

        add a word to the user dictionary ,example::

            一带一路 key

        需要作为关键词的，标引前缀必须为key

        :param word: 加入到临时用户词典重点词与词性，用空格分割
        :return: 1,true ; 0,false
        """
        return self.get_func('KeyExtract_AddUserWord', [c_char_p], c_int)(word)

    @NLPIRBase.byte_str_transform
    def clean_user_word(self) -> int:
        """
        Call **KeyExtract_CleanUserWord**

        Clean all temporary added user words

        :return: 1,true ; 0,false
        """
        return self.get_func('KeyExtract_CleanUserWord', None, c_int)()

    @NLPIRBase.byte_str_transform
    def save_the_usr_dict(self) -> int:
        """
        Call **KeyExtract_SaveTheUsrDic**

        Save dictionary to file

        :return: 1,true; 2,false
        """
        return self.get_func('KeyExtract_SaveTheUsrDic', None, c_int)()

    @NLPIRBase.byte_str_transform
    def del_usr_word(self, word: str) -> int:
        """
        Call **KeyExtract_DelUsrWord**

        delete a word from the user dictionary

        :param word:
        :return: -1, the word not exist in the user dictionary; else, the handle of the word deleted

        """
        return self.get_func('KeyExtract_DelUsrWord', [c_char_p], c_int)(word)

    @NLPIRBase.byte_str_transform
    def import_key_blacklist(self, filename: str, pos_blacklist: typing.Optional[str] = None) -> int:
        """
        Call **KeyExtract_ImportKeyBlackList**

        Import keyword black list

        import_blacklist will ass word to KeyBlackList.pdat remove the words form it need to backup it after use this function.
        this list of word will not affect the key word extract and segmentation

        
        :param filename: Text filename for user defined blacklist dictionary, each line for a stop keyword
        :param pos_blacklist: 停用的词性列表，即列为该词性列表访问的词不纳入关键词范围,如设置为#nr#ns#表示nr,ns不作为关键词
        :return: The number of lexical entry imported successfully
        """
        return self.get_func('KeyExtract_ImportKeyBlackList', [c_char_p, c_char_p], c_uint)(filename, pos_blacklist)

    """
    /*********************************************************************
    *
    以下函数为2013版本专门针对关键词批量发现的过程，一般建议脱机实现，不宜在线处理
    *********************************************************************/
    """

    @NLPIRBase.byte_str_transform
    def batch_start(self) -> int:
        """
        Call **KeyExtract_Batch_Start**

        启动关键词识别

        :return: true:success, false:fail
        """
        return self.get_func('KeyExtract_Batch_Start', None, c_int)()

    @NLPIRBase.byte_str_transform
    def batch_add_file(self, filename) -> int:
        """
        Call **KeyExtract_Batch_AddFile**

        往关键词识别系统中添加待识别关键词的文本文件,需要在运行KeyExtract_Batch_Start()之后，才有效
        
        :param filename: 文件名
        :return: bool, true:success, false:fail
        """
        return self.get_func('KeyExtract_Batch_AddFile', [c_char_p], c_ulong)(filename)

    @NLPIRBase.byte_str_transform
    def batch_addmen(self, txt: str) -> bool:
        """
        Call **KeyExtract_Batch_AddMem**
        往关键词识别系统中添加一段待识别关键词的内存,需要在运行KeyExtract_Batch_Start()之后，才有效

        :param txt: string
        :return: true:success, false:fail
        """
        return self.get_func('KeyExtract_Batch_AddMem', [c_char_p], c_bool)(txt)

    @NLPIRBase.byte_str_transform
    def batch_complete(self) -> int:
        """
        Call **KeyExtract_Batch_Complete**

        关键词识别添加内容结束,需要在运行KeyExtract_Batch_Start()之后，才有效

        :return: true:success, false:fail
        """
        return self.get_func('KeyExtract_Batch_Complete', None, c_int)()

    @NLPIRBase.byte_str_transform
    def batch_getresult(self, weight_out: bool = False) -> str:
        """
        Call **KeyExtract_Batch_GetResult**

        获取关键词识别的结果, 需要在运行KeyExtract_Batch_Complete()之后，才有效

        :param weight_out: 是否需要输出每个关键词的权重参数
        :return: 输出格式为:【关键词1】 【权重1】 【关键词2】 【权重2】 ...
        """
        return self.get_func('KeyExtract_Batch_GetResult', None, str)()

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        """
        Call **KeyExtract_GetLastErrorMsg**

        :return: error message
        """
        return self.get_func("KeyExtract_GetLastErrorMsg", None, c_char_p)()
