# -*- coding: utf-8 -*-
"""
HTML Export extensions of LOD database models
"""

from config.postgres.model_export import ExportWord, ExportDefinition
from config import DEFAULT_STYLE


class HTMLExportDefinition(ExportDefinition):

    @staticmethod
    def format_body(body: str) -> str:
        """
        Substitutes tags in the definition's body
        Formats punctuation signs
        :param body:
        :return:
        """
        to_key = '<k>'  # key
        tc_key = '</k>'
        to_log = '<l>'  # log
        tc_log = '</l>'

        return body \
            .replace("«", to_key).replace("»", tc_key) \
            .replace("{", to_log).replace("}", tc_log) \
            .replace("...", "…").replace("--", "—")

    @staticmethod
    def highlight_key(def_body, word) -> str:
        """
        Highlights the current key from the list, deselecting the rest
        :param def_body:
        :param word:
        :return:
        """

        to_key = '<k>'  # key
        tc_key = '</k>'

        word_template_original = f'{to_key}{word}{tc_key}'
        word_template_temp = f'<do_not_delete>{word}</do_not_delete>'
        def_body = def_body.replace(word_template_original, word_template_temp)
        def_body = def_body.replace(to_key, "").replace(tc_key, "")
        def_body = def_body.replace(word_template_temp, word_template_original)
        return def_body

    def export_for_english(self, word: str, style: str = DEFAULT_STYLE) -> str:
        """

        :param word:
        :param style:
        :return:
        """

        tags = {
            "normal": [
                '<span class="dg">(%s)</span>', '<span class="dt">[%s]</span> ', ' <span class="db">%s</span>',
                f'<span class="definition" id={self.id}>%s</span>', '<div class="d_line">%s</div>',
                '<span class="w_name">%s</span>, ', '<span class="w_origin">&lt;%s&gt;</span> ', ],
            "ultra": ['(%s)', '[%s] ', ' %s', '<d>%s</d>', '<ld>%s</ld>', '<wn>%s</wn>, ', '<o>&lt;%s&gt;</o> ', ],
        }
        t_d_gram, t_d_tags, t_d_body, t_def, t_def_line, t_word_name, t_word_origin = tags[style]

        gram_form = f'{str(self.slots) if self.slots else ""}' + self.grammar_code
        def_gram = t_d_gram % gram_form if gram_form else ''
        def_tags = t_d_tags % self.case_tags.replace("-", "&zwj;-&zwj;") if self.case_tags else ''

        def_body = HTMLExportDefinition.format_body(self.body)
        def_body = HTMLExportDefinition.highlight_key(def_body, word)
        def_body = t_d_body % def_body

        d_source_word = self.source_word
        w_name = d_source_word.name if not self.usage else self.usage.replace("%", d_source_word.name)
        word_name = t_word_name % w_name

        w_origin_x = d_source_word.origin_x if d_source_word.origin_x and d_source_word.type.group == "Cpx" else ''
        word_origin_x = t_word_origin % w_origin_x if w_origin_x else ''

        definition = t_def % f'{def_tags}{def_gram}{def_body}'
        return t_def_line % f'{word_name}{word_origin_x}{definition}'

    def export_for_loglan(self, style: str = DEFAULT_STYLE) -> str:
        """

        :param style:
        :return:
        """
        tags = {
            # usage, gram, body, tags, definition
            "normal": [
                '<span class="du">%s</span> ', '<span class="dg">(%s)</span> ', '<span class="db">%s</span>',
                ' <span class="dt">[%s]</span>', f'<div class="definition" id={self.id}>%s</div>', ],
            "ultra": ['<du>%s</du> ', '(%s) ', '%s', ' [%s]', '<d>%s</d>', ],
        }
        t_d_usage, t_d_gram, t_d_body, t_d_tags, t_definition = tags[style]

        def_usage = t_d_usage % self.usage.replace("%", "—") if self.usage else ''
        gram_form = f"{str(self.slots) if self.slots else ''}" + self.grammar_code
        def_gram = t_d_gram % gram_form if gram_form else ''
        def_body = t_d_body % HTMLExportDefinition.format_body(self.body)
        def_tags = t_d_tags % self.case_tags.replace("-", "&zwj;-&zwj;") if self.case_tags else ''
        return t_definition % f'{def_usage}{def_gram}{def_body}{def_tags}'


class HTMLExportWord(ExportWord):
    """

    """
    def html_origin(self, style: str = DEFAULT_STYLE):
        """

        :param style:
        :return:
        """
        o = self.origin
        ox = self.origin_x

        if (not o) and (not ox):
            return ''

        if not ox:
            origin = o
        elif not o:
            origin = ox
        else:
            origin = f'{o}={ox}'

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
        tags = {
            "normal": [
                '<span class="m_afx">%s</span> ', '<span class="m_match">%s</span> ',
                '<span class="m_type">%s</span> ', '<span class="m_author">%s</span> ',
                '<span class="m_year">%s</span> ', '<span class="m_rank">%s</span>',
                '<span class="m_use">%s</span>', '<span class="m_technical">%s</span>'],
            "ultra": ['<afx>%s</afx> ', '%s ', '%s ', '%s ', '%s ', '%s', '<use>%s</use>', '<tec>%s</tec>'],
        }
        t_afx, t_match, t_type, t_author, t_year, t_rank, t_use, t_technical = tags[style]

        html_affixes = t_afx % self.e_affixes if self.e_affixes else ''
        html_match = t_match % self.match if self.match else ''
        html_type = t_type % self.type.type if self.type.type else ''
        html_source = t_author % self.e_source if self.e_source else ''
        html_year = t_year % self.e_year if self.e_year else ''
        html_rank = t_rank % self.rank if self.rank else ''
        html_usedin = t_use % self.e_usedin.replace("| ", "|&nbsp;") if self.e_usedin else None

        html_tech = t_technical % f'{html_match}{html_type}{html_source}{html_year}{html_rank}'
        html_tech = f'{html_affixes}{self.html_origin(style)}{html_tech}'

        return {
                "mid": self.id,
                "technical": html_tech,
                "definitions": self.html_definitions(style),
                "used_in": html_usedin
        }
