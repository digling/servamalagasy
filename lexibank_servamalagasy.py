from pathlib import Path
from pylexibank.dataset import Dataset as BaseDataset 
from pylexibank import Language, Concept, FormSpec
from pylexibank import progressbar

from clldutils.misc import slug
import attr


@attr.s
class CustomLanguage(Language):
    FileName = attr.ib(default=None)
    Number = attr.ib(default=None)
    Area = attr.ib(default=None)
    


@attr.s
class CustomConcept(Concept):
    Number = attr.ib(default=None)
    Italian_Gloss = attr.ib(default=None)
    French_Gloss = attr.ib(default=None)
    Malagasy_Gloss = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "servamalagasy"
    concept_class = CustomConcept
    language_class = CustomLanguage
    #form_spec = FormSpec(
    #        missing_data=("---", ),
    #        separators="/",
    #        replacements=[(" ", "_")]
    #        )

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """
        concepts = {}
        for concept in self.concepts:
            cid = '{0}_{1}'.format(concept['NUMBER'], slug(concept['ENGLISH']))
            args.writer.add_concept(
                    ID=cid,
                    Name=concept['ENGLISH'],
                    Number=concept['NUMBER'],
                    Italian_Gloss=concept['ITALIAN'],
                    French_Gloss=concept['FRENCH'],
                    Malagasy_Gloss=concept['MALAGASY'],
                    Concepticon_ID=concept['CONCEPTICON_ID'],
                    Concepticon_Gloss=concept['CONCEPTICON_GLOSS']
                    )
            concepts[concept['FRENCH']] = cid
        languages = {}
        for language in self.languages:
            args.writer.add_language(
                    ID=language['ID'],
                    Name=language['Name'],
                    Latitude=language['Latitude'],
                    Longitude=language['Longitude'],
                    Area=language['Area'],
                    Number=language['Number'],
                    Glottocode=language['Glottocode']
                    )
            languages[language['FileName']] = language['ID']
        args.writer.add_sources()
        for row in progressbar(self.raw_dir.read_csv('data.tsv', delimiter='\t',
                dicts=True)):
            args.writer.add_form(
                    Language_ID=languages[row['FILENAME']],
                    Parameter_ID=concepts[row['FRENCH']],
                    Value=row['FORM'],
                    Form=row['FORM'],
                    Source='Serva2020'
                    )
