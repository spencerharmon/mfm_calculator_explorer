
class Breadcrumb():
    def __init__(self,**kwargs):
        try:
            self.separator = kwargs['separator']
        except KeyError:
            self.separator = ' > '

        try:
            self.paths = kwargs['url_dict']
        except KeyError:
            self.paths = []

    def add(self,hgrchy):
        self.path.append(hgrchy)

    def gen(self):
        ''' return markup as string '''
        html_list = []
        for name,path in self.paths.items():
            html_list.append(r'<a href={0}>{1}</a>'.format(path,name))
        return self.separator.join(html_list)
