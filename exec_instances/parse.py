
# parses mfm log file and inputs into database

import re

from django.core.urlresolvers import reverse

from .models import *

class Parse:
    def __init__(self,files,title):
        self.exec_instance = ExecInstance()
        self.exec_instance.title = title
        self.exec_instance.save()
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
            exec_instance.delete()
            raise self.error

    def __str__(self):
        return self.files

    def __repr__(self):
        return self.files

    def parse(self,file):
        aeps = AEPS()
        aeps.aeps = self.get_aeps(file)
        aeps.exec_instance = self.exec_instance
        aeps.save()
        try:
            for line in file:
                decoded_line = line.decode('UTF-8')
                self.parse_line(decoded_line,aeps)
            self.parse_sanity_check(file,aeps)
        except ParseError:
            aeps.delete()
            raise

    def parse_line(self,line,aeps):
        p_grid_size = re.compile(r'^DefineGridSize\((?P<x_size>[0-9]+),(?P<y_size>[0-9]+),[0-9]+,[0-9]+\)$')
        p_register_element = re.compile(r'^RegisterElement\(Ue[0-9]+(?P<element_name>[A-Za-z]+)10-[0-9]+,(?P<element_id>T[A-F0-9]+)\)$')
        p_site = re.compile(r'^Site\((?P<x>[0-9]+),(?P<y>[0-9]+),[A-F0-9]+,(?P<atom_type>T[A-F0-9]+),(?P<atom_value>[A-F0-9]+),.*\)$')
        p_log_message = re.compile(r'^\s+PP\(txln="[0-9]+-[0-9]+:\s\b(?P<actual_aeps>[0-9]+AEPS)\b\s\[[0-9A-F]+\]MSG:\s(?P<message>.*)\"\)')

        m_grid_size = p_grid_size.search(line)
        m_register_element = p_register_element.search(line)
        m_site = p_site.search(line)
        m_log_message = p_log_message.search(line)

        if m_grid_size:
            x = int(m_grid_size.group('x_size'))
            y = int(m_grid_size.group('y_size'))
            self.exec_instance.grid_size = x * y
            self.exec_instance.save()

        elif m_register_element:
            registered_element = RegisteredElement()
            registered_element.exec_instance = self.exec_instance
            registered_element.element_name = m_register_element.group('element_name')
            registered_element.element_id = m_register_element.group('element_id')
            registered_element.save()
        elif m_site:
            site = Site()
            site.aeps = aeps
            site.x = m_site.group('x')
            site.y = m_site.group('y')
            site.atom_type = m_site.group('atom_type')
            site.val = m_site.group('atom_value')
            site.save()
        elif m_log_message:
            log_message = LogMessage()
            log_message.aeps = aeps
            log_message.actual_aeps = m_log_message.group('actual_aeps')
            log_message.message = m_log_message.group('message')
            log_message.save()

    def parse_sanity_check(self,file,aeps):
        try:
            self.site_count_check(file,aeps)
        except ParseError:
            raise

    def site_count_check(self,file,aeps):
        if self.exec_instance.grid_size != aeps.site_set.count():
            raise ParseError(
                'File {0} failed site count check.'
                'Grid Size: {1}'
                'Sites Found: {2}'
                .format(
                    file.name,
                    self.exec_instance.grid_size,
                    aeps.site_set.count()
                )
            )
        elif self.exec_instance.grid_size == 0:
            raise ParseError('Site count check could not determine grid size.')
        elif aeps.site_set.count() == 0:
            raise ParseError('No sites found.')
        else:
            return

    def construct_redirect_url(self):
        ret = reverse('exec_instances:exec_instances')
        ret += self.exec_instance.title
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
