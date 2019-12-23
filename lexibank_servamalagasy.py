import re
from pathlib import Path

from bs4 import BeautifulSoup
from csvw import UnicodeWriter

import pylexibank
from clldutils.misc import slug

URL1 = 'http://people.disim.univaq.it/~serva/languages/malgasce.htm'
URL2 = 'http://people.disim.univaq.it/~serva/languages/english.html'


class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "servamalagasy"

    def cmd_download(self, args):
        with self.raw_dir.temp_download(URL1, 'temp') as f:
            soup = BeautifulSoup(f.read_text(encoding="utf8"), 'html.parser')
            with UnicodeWriter(self.raw_dir / 'malgasce.csv') as out:
                for tr in soup.find('table').find_all('tr'):
                    out.writerow([td.get_text().strip() for td in tr.find_all('td')])
        
        with self.raw_dir.temp_download(URL2, 'temp') as f:
            soup = BeautifulSoup(f.read_text(encoding="utf8"), 'html.parser')
            with UnicodeWriter(self.raw_dir / 'concepts.csv') as out:
                out.writerow(['ID', 'GLOSS', 'CONCEPTICON_ID'])
                for tr in soup.find('table').find_all('tr'):
                    no, gloss = [c.get_text().strip() for c in tr.find_all('td')]
                    try:
                        int(no)
                        out.writerow([no, re.sub('\s+', ' ', gloss), ''])
                    except:
                        pass
    
    def cmd_makecldf(self, args):
        args.writer.add_sources()
        languages = args.writer.add_languages(lookup_factory="Name")
        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english),
            lookup_factory=lambda c: int(c['ID'].split("_")[0])
        )
        for row in self.raw_dir.read_csv('malgasce.csv', dicts=True):
            cid = int(row.pop(""))
            for language in row:
                lex = args.writer.add_forms_from_value(
                    Language_ID=languages[language],
                    Parameter_ID=concepts[cid],
                    Value=row[language],
                    Source=['Serva2011']
                )
