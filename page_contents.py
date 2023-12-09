class PageContents:
    
    # Parse a markdown file contents into memory
    def __init__(self, file, filename):
        # url
        line = file.readline().strip()
        if line == '---' or line == '':
            raise SyntaxError(f'Expected local URL in {filename}, instead found {line}')
        self.url = line

        # title
        line = file.readline().strip()
        if line == '---' or line == '':
            raise SyntaxError(f'Expected title in {filename}, instead found {line}')
        self.title = line

        # tags
        line = file.readline().strip()
        if line == '---' or line == '':
            raise SyntaxError(f'Expected tags in {filename}, instead found {line}')
        self.tags = []
        for tag in line.split(','):
            self.tags.append(tag.strip())

        # date (optional)
        sep_encountered = False
        self.datestring = None
        line = file.readline().strip()
        if line == '---':
            sep_encountered = True
        else:
            if line == '':
                raise SyntaxError(f'Date line invalid in {filename}, found {line}')
            self.datestring = line

        # image (optional)
        self.image_url = None
        self.image_alt = None
        if not sep_encountered:
            line = file.readline().strip()
            if line == '---':
                sep_encountered = True
            else:
                # ensure proper line format
                ind_0 = line.find('!')
                ind_1 = line.find('[')
                ind_2 = line.find(']')
                ind_3 = line.find('(')
                ind_4 = line.find(')')
                if (not (ind_0 < ind_1 < ind_2 < ind_3 < ind_4)) and ind_1 == 1:
                    raise SyntaxError(f'Article image line invalid in {filename}, found {line}')
                self.image_alt = line[ind_1 + 1 : ind_2]
                self.image_url = line[ind_3 + 1 : ind_4]

        if not sep_encountered:
            file.readline()

        # md contents
        self.contents = file.read()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'[{self.url} {self.title} {self.tags} {self.datestring} {self.image_url}]\n{self.contents}'

    def get_line_count(self):
        return self.contents.count('\n') + 1

