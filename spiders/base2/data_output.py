#!/usr/bin/env python3


import os
import time
import codecs

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class DataOutput:
    def __init__(self):
        if not os.path.exists('dist'):
            os.mkdir('dist')
        filename = 'baike_%s.html' % (time.strftime(
            '%Y-%m-%d-%H-%M-%S', time.localtime()
        ))

        self.filepath = os.path.join('dist', filename)
        self.output_head(self.filepath)
        self.datas = []

    def output_head(self, path):
        """写入HTML头"""
        fout = codecs.open(path, 'w', encoding='utf-8')
        fout.write('<html>')
        fout.write("<head><meta charset='utf-8'/> </head>")
        fout.write('<body>')
        fout.write('<table border="1">')
        fout.write('<tr>')
        fout.write('<th>%s</td>' % 'Link')
        fout.write('<th>%s</td>' % 'Title')
        fout.write('<th>%s</td>' % 'Summary')
        fout.write('</tr>')
        fout.close()

    def output_end(self, path):
        fout = codecs.open(path, 'a', encoding='utf-8')
        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
        fout.close()

    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)
        if len(self.datas) > 10:
            self.output_html(self.filepath)

    def flush_data(self):
        if len(self.datas) != 0:
            self.output_html(self.filepath)

    def output_html(self, path):
        fout = codecs.open(path, 'a', encoding='utf-8')
        for data in self.datas:
            fout.write('<tr>')
            fout.write('<td>%s</td>' % data['url'])
            fout.write('<td>%s</td>' % data['title'])
            fout.write('<td>%s</td>' % data['summary'])
            fout.write('</tr>')
            self.datas.remove(data)

        fout.close()
