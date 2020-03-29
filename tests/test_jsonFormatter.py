import jsonFormatter
import json
import testsHelper as Hlp  # TODO: Think about this problem with 'No module...' err
import pytest


#################################################################################################
# Serialization tests
#################################################################################################

@pytest.mark.parametrize('timeDigitsTupList, resultFilePath',
                         [
                             ([([20, 3, 8], [20, 3, 18])], 'test_data/t1.json'),
                             ([([20, 3, 8], [20, 3, 18]), ([20, 3, 22], [20, 3, 24])], 'test_data/t2.json')

                         ])
def test_serialization_timestamps(timeDigitsTupList, resultFilePath):
    # arrange
    appList = [Hlp.createBasicApp(timeDigitsTupList, 'youtube.com', 'opera')]
    expected_result = Hlp.getResultFromFile(resultFilePath)

    # act
    encodedList = json.dumps(appList, cls=jsonFormatter.CustomJsonEncoder)

    # assert
    assert Hlp.removeWhitespacesFromString(encodedList) == Hlp.removeWhitespacesFromString(expected_result)


def test_serialization_instances():
    # arrange
    app = Hlp.createBasicApp([([20, 3, 8], [20, 3, 18])], 'youtube.com', 'opera')
    di2 = Hlp.createDetailedInstance([([20, 5, 0], [20, 5, 30])], '9gag.com')
    app.updateOrAddInstance(di2)
    appList = [app]

    expected_result = Hlp.getResultFromFile('test_data/t3.json')

    # act
    encodedList = json.dumps(appList, cls=jsonFormatter.CustomJsonEncoder)

    # assert
    assert Hlp.removeWhitespacesFromString(encodedList) == Hlp.removeWhitespacesFromString(expected_result)


def test_serialization_apps():
    # arrange
    app = Hlp.createBasicApp([([20, 3, 8], [20, 3, 10])], 'youtube.com', 'opera')
    app2 = Hlp.createBasicApp([([20, 7, 10], [20, 7, 30])], 'MyNovelFinalEditLast7.docx', 'word')
    appList = [app, app2]

    expected_result = Hlp.getResultFromFile('test_data/t4.json')

    # act
    encodedList = json.dumps(appList, cls=jsonFormatter.CustomJsonEncoder)

    # assert
    assert Hlp.removeWhitespacesFromString(encodedList) == Hlp.removeWhitespacesFromString(expected_result)


#################################################################################################
# Deserialization tests
#################################################################################################

@pytest.mark.parametrize('inputFilePath, timeDigitsTupList',
                         [
                             ('test_data/t1.json', [([20, 3, 8], [20, 3, 18])]),
                             ('test_data/t2.json', [([20, 3, 8], [20, 3, 18]), ([20, 3, 22], [20, 3, 24])])

                         ])
def test_deserialization_timestamps(inputFilePath, timeDigitsTupList):
    # arrange
    expectedAppList = [Hlp.createBasicApp(timeDigitsTupList, 'youtube.com', 'opera')]
    appList = []

    # act
    with open(inputFilePath) as input_file:
        appList = json.load(input_file, cls=jsonFormatter.CustomJsonDecoder)

    # assert
    assert appList == expectedAppList


def test_deserialization_instances():
    # arrange
    app = Hlp.createBasicApp([([20, 3, 8], [20, 3, 18])], 'youtube.com', 'opera')
    di2 = Hlp.createDetailedInstance([([20, 5, 0], [20, 5, 30])], '9gag.com')

    app.updateOrAddInstance(di2)
    expectedAppList = [app]
    appList = []

    # act
    with open('test_data/t3.json') as input_file:
        appList = json.load(input_file, cls=jsonFormatter.CustomJsonDecoder)

    # assert
    assert appList == expectedAppList


def test_deserialization_apps():
    # arrange
    app = Hlp.createBasicApp([([20, 3, 8], [20, 3, 10])], 'youtube.com', 'opera')
    app2 = Hlp.createBasicApp([([20, 7, 10], [20, 7, 30])], 'MyNovelFinalEditLast7.docx', 'word')
    expectedAppList = [app, app2]
    appList = []

    # act
    with open('test_data/t4.json') as input_file:
        appList = json.load(input_file, cls=jsonFormatter.CustomJsonDecoder)

    # assert
    assert appList == expectedAppList
