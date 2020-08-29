# -*- coding: utf-8 -*-
"""
HTML Export extensions of LOD database models
"""

from config.postgres.model_export import ExportWord, ExportDefinition
from config import DEFAULT_STYLE


class HTMLExportDefinition(ExportDefinition):

    @staticmethod
    def body_replacer(body: str):
        """

        :param body:
        :return:
        """
        open_key_tag = '<k>'  # key
        close_key_tag = '</k>'
        open_log_tag = '<l>'  # log
        close_log_tag = '</l>'

        return body \
            .replace("«", open_key_tag) \
            .replace("»", close_key_tag) \
            .replace("{", open_log_tag) \
            .replace("}", close_log_tag) \
            .replace("...", "…").replace("--", "—")

    def export_for_english(self, word: str, style: str = DEFAULT_STYLE):
        """

        :param word:
        :param style:
        :return:
        """
        gram_form = f'{str(self.slots) if self.slots else ""}' + self.grammar_code
        def_gram = f'({gram_form})' if gram_form else ''
        def_tags = f'[{self.case_tags.replace("-", "&zwj;-&zwj;")}] ' if self.case_tags else ''
        d_source_word = self.source_word

        word_template_original = f'<k>{word}</k>'
        word_template_temp = f'<do_not_delete>{word}</do_not_delete>'
        def_body = f' {HTMLExportDefinition.body_replacer(self.body)}'
        def_body = def_body.replace(word_template_original, word_template_temp)
        def_body = def_body.replace("<k>", "").replace("</k>", "")
        def_body = def_body.replace(word_template_temp, word_template_original)

        word_name = f'<wn>{d_source_word.name if not self.usage else self.usage.replace("%", d_source_word.name)}</wn>, '
        w_origin_x = d_source_word.origin_x if d_source_word.origin_x and d_source_word.type.group == "Cpx" else ''
        word_origin_x = f'<o>&lt;{w_origin_x}&gt;</o> ' if w_origin_x else ''
        return f'<ld>{word_name}{word_origin_x}<d>{def_tags}{def_gram}{def_body}</d></ld>'

    def export_for_loglan(self, style: str = DEFAULT_STYLE):
        """

        :param style:
        :return:
        """
        tags_open = {
            "normal": [
                '<span class="du">', '<span class="dg">', '<span class="db">',
                '<span class="dt">', f'<div class="d" id={self.id}>', ],
            "ultra": ['<du>', '', '', '', '<d>', ],
        }
        tags_close = {
            "normal": ['</span>', '</span>', '</span>', '</span>', '</div>', ],
            "ultra": ['</du>', '', '', '', '</d>', ],
        }

        to_d_usage, to_d_gram, to_d_body, to_d_tags, to_definition = tags_open[style]
        tc_d_usage, tc_d_gram, tc_d_body, tc_d_tags, tc_definition = tags_close[style]

        def_usage = f'{to_d_usage}{self.usage}{tc_d_usage} '.replace("%", "—") if self.usage else ''
        gram_form = f"{str(self.slots) if self.slots else ''}" + self.grammar_code
        def_gram = f'({to_d_gram}{gram_form}{tc_d_gram}) ' if gram_form else ''
        def_body = f'{to_d_body}{HTMLExportDefinition.body_replacer(self.body)}{tc_d_body}'
        def_tags = f' {to_d_tags}[{self.case_tags.replace("-", "&zwj;-&zwj;")}]{tc_d_tags}' if self.case_tags else ''
        return f'{to_definition}{def_usage}{def_gram}{def_body}{def_tags}{tc_definition}'


class HTMLExportWord(ExportWord):
    """

    """
    def html_origin(self, style: str = DEFAULT_STYLE):
        """

        :param style:
        :return:
        """
        if (not self.origin) and (not self.origin_x):
            return ''

        if not self.origin_x:
            origin = self.origin
        elif not self.origin:
            origin = self.origin_x
        else:
            origin = f'{self.origin}={self.origin_x}'

        if style == "normal":
            return f'<span class="m_origin">&lt;{origin}&gt;</span> '
        else:
            return f'<o>&lt;{origin}&gt;</o> '

    def html_definitions(self, style: str = DEFAULT_STYLE):
        """

        :param style:
        :return:
        """
        return [HTMLExportDefinition.export_for_loglan(d, style=style) for d in self.definitions]

    def meaning(self, style: str = DEFAULT_STYLE) -> dict:
        """

        :param style:
        :return:
        """
        tags_open = {
            "normal": [
                '<span class="m_afx">', '<span class="m_match">', '<span class="m_type">',
                '<span class="m_author">', '<span class="m_year">', '<span class="m_rank">',
                '<span class="m_use">', '<span class="m_technical">'],
            "ultra": ['<afx>', '', '', '', '', '', '<use>', '<tec>'],
        }
        tags_close = {
            "normal": ['</span>', '</span>', '</span>', '</span>', '</span>', '</span>', '</span>', '</span>'],
            "ultra": ['</afx>', '', '', '', '', '', '</use>', '</tec>'],
        }

        to_afx, to_match, to_type, to_author, to_year, to_rank, to_use, to_technical = tags_open[style]
        tc_afx, tc_match, tc_type, tc_author, tc_year, tc_rank, tc_use, tc_technical = tags_close[style]

        html_affixes = f'{to_afx}{self.e_affixes}{tc_afx} ' if self.e_affixes else ''
        html_match = f'{to_match}{self.match}{tc_match} ' if self.match else ''
        html_type = f'{to_type}{self.type.type}{tc_type} ' if self.type.type else ''
        html_source = f'{to_author}{self.e_source}{tc_author} ' if self.e_source else ''
        html_year = f'{to_year}{self.e_year}{tc_year} ' if self.e_year else ''
        html_rank = f'{to_rank}{self.rank}{tc_rank}' if self.rank else ''
        html_usedin = f'{to_use}{self.e_usedin.replace("| ", "|&nbsp;")}{tc_use}' if self.e_usedin else None

        html_tech = f'{to_technical}{html_match}{html_type}{html_source}{html_year}{html_rank}{tc_technical}'
        html_tech = f'{html_affixes}{self.html_origin(style)}{html_tech}'

        return {
                "mid": self.id,
                "technical": html_tech,
                "definitions": self.html_definitions(style),
                "used_in": html_usedin
        }
