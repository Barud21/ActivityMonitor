import jsonOperations
import pytest
import tests.testsHelper as Hlp


#################################################################################################
# Decoding json tests
#################################################################################################

# @pytest.mark.parametrize(
#                         [
#                             'test_data/t1.json',
#                             'test_data/t2.json'
#                         ])
# def test_DecodingJson():
    # arrange




#################################################################################################
# Summing up total time test
#################################################################################################

@pytest.mark.parametrize('jsonName, result',
                         [
                             ('test_data/t1.json', [('opera', 10)]),
                             ('test_data/t2.json', [('opera', 12)]),
                             ('test_data/t3.json', [('opera', 40)]),
                             ('test_data/t4.json', [('word', 20), ('opera', 2)])
                         ])
def test_SummingUpTotalTime(jsonName, result):
    # arrange
    expectedTotalTime = result
    applicationList = Hlp.decodeJson(jsonName, __file__)

    # act
    summedTotalTime = jsonOperations.defSummingUpTotalTime(applicationList)

    # assert
    assert summedTotalTime == expectedTotalTime

#################################################################################################
# Calculating pecentage time of use test
#################################################################################################

@pytest.mark.parametrize('totalTimeForApplication, result',
                         [
                             ([('opera', 10)], [100]),
                             ([('opera', 40), ('word', 10)], [80, 20]),
                             ([('opera', 30), ('word', 10)], [75, 25]),
                             ([('opera', 25), ('word', 15), ('note', 10)], [50, 30, 20])
                         ])
def test_PercentageCalculation(totalTimeForApplication, result):
    # arrange
    expectedPercentageOfTime = result

    # act
    PercentageOfUse = jsonOperations.defPercentageCalculation(totalTimeForApplication)

    # assert
    assert PercentageOfUse == expectedPercentageOfTime

#################################################################################################
# Sorting instances test
#################################################################################################

@pytest.mark.parametrize('jsonName, result',
                         [
                             ('test_data/t1.json', {'opera': [('youtube.com', 10)]}),
                             ('test_data/t2.json', {'opera': [('youtube.com', 12)]}),
                             ('test_data/t3.json', {'opera': [('9gag.com', 30), ('youtube.com', 10)]}),
                             ('test_data/t4.json', {'opera': [('youtube.com', 2)], 'word': [('MyNovelFinalEditLast7.docx', 20)]})
                         ])
def test_SortedInstances(jsonName, result):
    # arrange
    expectedSortedInstances = result
    applicationList = Hlp.decodeJson(jsonName, __file__)

    # act
    SortedInstances = jsonOperations.defSortedInstances(applicationList)

    # assert
    assert SortedInstances == expectedSortedInstances