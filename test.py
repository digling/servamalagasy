
def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)


def test_parameters(cldf_dataset):
    assert len(list(cldf_dataset["ParameterTable"])) == 200


def test_languages(cldf_dataset):
    assert len(list(cldf_dataset["LanguageTable"])) == 24


def test_forms(cldf_dataset):
    f = [
        f for f in cldf_dataset["FormTable"] if f["Form"] == 'fo'
    ]
    assert len(f) == 24


def test_cognates(cldf_dataset):
    len(list(cldf_dataset["CognateTable"])) == 0  # no cognates
