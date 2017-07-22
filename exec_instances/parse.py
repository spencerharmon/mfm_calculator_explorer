
# parses mfm log file and inputs into database

import re

from django.core.urlresolvers import reverse

from .models import *

class Parse:
    def __init__(self,files,title):
        self.model_list = [ ExecInstance() ]
        self.model_list[0].title = title
        self.files = files
        self.redirect_url = self.construct_redirect_url()
        self.error = None
        for file in self.files:
            try:
                self.parse(file)
            except ParseError as e:
                self.error = e
                break
        if self.error is not None:
            raise self.error

    def __str__(self):
        return self.files

    def __repr__(self):
        return self.files

    def parse(self,file):
        aeps = AEPS()
        aeps.aeps = self.get_aeps(file)
        aeps.exec_instance = self.model_list[0]

        try:
            for line in file:
                self.parse_line(str(line),aeps)
            self.parse_sanity_check(file,aeps)
            raise ParseError('works when called from parse')
        except ParseError:
            raise
        finally: #only for testing; should be else: no need to perform action if sanity check failed
            self.model_list.append(aeps)

    def parse_line(self,line,aeps):
        p_grid_size = re.compile(r'^DefineGridSize\((?P<x_size>[0-9]+),(?P<y_size>[0-9]+),[0-9]+,[0-9]+\)$')
        p_register_element = re.compile(r'^RegisterElement\(Ue[0-9]+(?P<element_name>[A-Za-z]+)10-[0-9]+,(?P<element_id>\W)\)$')
        p_site = re.compile(r'^Site\((?P<x>[0-9]+),(?P<y>[0-9]+),\W*,(?P<atom_type>[A-F0-9]+),(?P<atom_value>[A-F0-9]).*\)$')
        p_log_message = re.compile(r'^\s+PP\(txln="[0-9]+-[0-9]+:\s\b(?P<actual_aeps>AEPS[0-9]+)\b.*MSG:\s(?P<message>.*)\"\)')

        m_grid_size = p_grid_size.search(line)
        m_register_element = p_register_element.search(line)
        m_site = p_site.search(line)
        m_log_message = p_log_message.search(line)

        if m_grid_size:
            self.model_list[0].grid_size = m_grid_size.group('x_size') * m_grid_size.group('y_size')

        elif m_register_element:
            registered_element = RegisterElement()
            registered_element.exec_instance = self.model_list[0]
            registered_element.element_name = m_register_element.group('element_name')
            registered_element.element_id = m_register_element.group('element_id')

            self.model_list.append(registered_element)

        elif m_site:
            site = Site()
            site.aeps = aeps
            site.x = m_site.group('x')
            site.y = m_site.group('y')
            site.atom_type = m_site.group('atom_type')
            site.val = m_site.group('atom_value')

            self.model_list.append(site)

        elif m_log_message:
            log_message = LogMessage()
            log_message.aeps = aeps
            log_message.actual_aeps = m_log_message.group('actual_aeps')
            log_message.message = m_log_message.group('message')

            self.model_list.append(log_message)

    def parse_sanity_check(self,file,aeps):
        try:
            self.site_count_check(file,aeps)
        except ParseError:
            raise

    def site_count_check(self,file,aeps):
        if self.model_list[0].grid_size != aeps.site_set.count():
            raise ParseError('File %s failed site count check' % file.name)
        elif self.model_list[0].grid_size == 0:
            raise ParseError('Site count check could not determine grid size.')
        elif aeps.site_set.count() == 0:
            raise ParseError('No sites found.')
        else:
            return

    def construct_redirect_url(self):
        ret = reverse('exec_instances:exec_instances')
        ret += self.model_list[0].title
        ret += "/"
        return ret

    def get_aeps(self,file):
        pattern = re.compile(r'[0-9]+-(?P<aeps>[0-9]+)\.mfs$')
        match = pattern.search(file.name)
        if match:
            return match.group('aeps')
        else:
            raise ParseError

class ParseError(Exception):
    '''Raise for all parse errors'''

class LineParseError(ParseError):
    '''Raise for all errors parsing a line'''
