from janome.charfilter import *
from janome.analyzer import Analyzer
from janome.tokenizer import Tokenizer
from janome.tokenfilter import *
from gensim import corpora
import re

USERNAME_PREFIX_REGEX = r'^@.+\s'
user_regex = re.compile(USERNAME_PREFIX_REGEX)


tokenizer = Tokenizer()

class NumericReplaceFilter(TokenFilter):
    """
    名詞中の数(漢数字を含む)を全て0に置き換えるTokenFilterの実装
    """

    def apply(self, tokens):
        for token in tokens:
            parts = token.part_of_speech.split(',')
            if (parts[0] == '名詞' and parts[1] == '数'):
                token.surface = '0'
                token.base_form = '0'
                token.reading = 'ゼロ'
                token.phonetic = 'ゼロ'

            yield token



class Wakati(object):
    char_filters = [UnicodeNormalizeCharFilter(),  # UnicodeをNFKC(デフォルト)で正規化
                    RegexReplaceCharFilter('http[a-z!-/:-@[-`{-~]', ''),  # urlの削除
                    RegexReplaceCharFilter('@[a-zA-Z]+', ''),  # @ユーザ名の削除
                    RegexReplaceCharFilter('[!-/:-@[-`{-~♪♫♣♂✨дд∴∀♡☺➡〃∩∧⊂⌒゚≪≫•°。、♥❤◝◜◉◉★☆✊≡ø彡「」『』○≦∇✿╹◡✌]', ''),
                    RegexReplaceCharFilter('\n', '')
                    # 記号の削除
                    RegexReplaceCharFilter('\u200b', ''),  # 空白の削除                     # 検索キーワードの削除
                    ]
    token_filters = [NumericReplaceFilter(),  # 名詞中の漢数字を含む数字を0に置換
                     CompoundNounFilter(),  # 名詞が連続する場合は複合名詞にする
                     POSKeepFilter(['名詞']),  # 名詞・動詞・形容詞・副詞のみを取得する
                     LowerCaseFilter(),  # 英字は小文字にする
                     ]
    analyzer = Analyzer(char_filters, tokenizer, token_filters)

    def __init__(self):
        self.corpus = []





