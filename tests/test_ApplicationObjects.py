import testsHelper as Hlp
import pytest

#################################################################################################
# TimeStamp tests
#################################################################################################


@pytest.mark.parametrize('timeDigitsTup, expectedResult',
                         [
                             (([20, 3, 8], [20, 3, 8]), 0),
                             (([20, 3, 8], [20, 3, 18]), 10),
                             (([20, 3, 8], [21, 3, 8]), 3600)

                         ])
def test_TS_calculateTimeDiff(timeDigitsTup, expectedResult):
    # arrange
    ts = Hlp.createTimestamp(timeDigitsTup)

    # act
    result = ts.calculateTimeDiffInSecs()

    # assert
    assert result == expectedResult


def test_TS_equality():
    # arrange
    ts1 = Hlp.createTimestamp(([20, 3, 8], [20, 3, 8]))
    ts2 = Hlp.createTimestamp(([20, 3, 8], [20, 3, 8]))
    ts3 = Hlp.createTimestamp(([21, 10, 8], [22, 0, 0]))

    # act
    # well, not this time my friend ;)

    # assert
    assert ts1 == ts2
    assert ts1 != ts3


#################################################################################################
# DetailedInstance tests
#################################################################################################


@pytest.mark.parametrize('timeDigitsTupList, expectedResult',
                         [
                             ([([20, 3, 8], [20, 3, 8])], 0),
                             ([([20, 3, 8], [20, 3, 18])], 10),
                             ([([20, 3, 8], [21, 3, 8])], 3600),
                             ([([20, 3, 8], [21, 3, 8]), ([22, 0, 0], [23, 0, 0])], 7200)
                         ])
def test_DI_totalTimeInNew(timeDigitsTupList, expectedResult):
    # arrange
    di = Hlp.createDetailedInstance(timeDigitsTupList, 'youtube')

    # act
    totalTime = di.totalTime

    # assert
    assert totalTime == expectedResult


# TODO: maybe more friendly parameters, so we don't have to keep in mind that 10sec for the initial timestamp?
@pytest.mark.parametrize('newTimestampDigits, expectedTimestampsCount, expectedTotalTime',
                         [
                             (([20, 0, 0], [20, 0, 10]), 1, 10),
                             (([20, 4, 0], [20, 4, 30]), 2, 40)
                         ])
def test_DI_addingNewTimetamp(newTimestampDigits, expectedTimestampsCount, expectedTotalTime):
    # arrange
    di = Hlp.createDetailedInstance([([20, 0, 0], [20, 0, 10])], 'youtube')

    # act
    di.addTimeStamp(Hlp.createTimestamp(newTimestampDigits))

    # assert
    assert len(di.timestamps) == expectedTimestampsCount
    assert di.totalTime == expectedTotalTime


#################################################################################################
# ApplicationWithInstances tests
#################################################################################################


def test_AWI_updateExistingInstance():
    # arrange
    app = Hlp.createBasicApp([([20, 0, 0], [20, 0, 10])], 'youtube.com', 'opera')
    di = Hlp.createDetailedInstance([([20, 30, 0], [20, 30, 30])], 'youtube.com')

    # act
    app.updateOrAddInstance(di)

    # assert
    assert len(app.instances) == 1
    assert len(app.instances[0].timestamps) == 2
    assert app.instances[0].totalTime == 40


def test_AWI_addNewInstance():
    # arrange
    app = Hlp.createBasicApp([([20, 0, 0], [20, 0, 10])], 'youtube.com', 'opera')
    di = Hlp.createDetailedInstance([([19, 30, 0], [19, 31, 0])], 'howtostaycool.com')

    # act
    app.updateOrAddInstance(di)

    # assert
    assert len(app.instances) == 2
    assert len(app.instances[0].timestamps) == 1
    assert len(app.instances[1].timestamps) == 1

    assert app.instances[0].totalTime == 10
    assert app.instances[1].totalTime == 60


def test_AWI_updateBasedOnOtherAppSameInstances():
    # arrange
    app1 = Hlp.createBasicApp([([20, 0, 0], [20, 0, 10])], 'youtube.com', 'opera')
    app2 = Hlp.createBasicApp([([20, 10, 0], [20, 10, 30])], 'youtube.com', 'opera')

    # act
    app1.updateBasedOnOther(app2)

    # assert
    assert len(app1.instances) == 1
    assert len(app1.instances[0].timestamps) == 2
    assert app1.instances[0].totalTime == 40

    assert len(app2.instances[0].timestamps) == 1
    assert app2.instances[0].totalTime == 30


def test_AWI_updateBasedOnOtherAppDifferentIsntances():
    # arrange
    app1 = Hlp.createBasicApp([([20, 0, 0], [20, 0, 10])], 'youtube.com', 'opera')
    app2 = Hlp.createBasicApp([([20, 10, 0], [20, 10, 30])], 'howtostaycool.com', 'opera')

    # act
    app1.updateBasedOnOther(app2)

    # assert
    assert len(app1.instances) == 2
    assert len(app1.instances[0].timestamps) == 1
    assert len(app1.instances[1].timestamps) == 1
    assert app1.instances[0].totalTime == 10
    assert app1.instances[1].totalTime == 30

    assert len(app2.instances) == 1
    assert len(app2.instances[0].timestamps) == 1


def test_AWI_updateBasedOnOtherAppDifferentAppName():
    # arrange
    app1 = Hlp.createBasicApp([([20, 0, 0], [20, 0, 10])], 'youtube.com', 'opera')
    app2 = Hlp.createBasicApp([([20, 10, 0], [20, 10, 30])], 'youtube.com', 'chrome')

    # act
    app1.updateBasedOnOther(app2)

    # assert
    assert len(app1.instances) == 1
    assert len(app1.instances[0].timestamps) == 1

    assert len(app2.instances) == 1
    assert len(app2.instances[0].timestamps) == 1


# TODO: Bartek: Add test(s) for sumOfTotalTimeForApplication