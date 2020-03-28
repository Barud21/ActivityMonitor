import ApplicationObjects as Ao
import helper as Hlp
import pytest

#################################################################################################
# TimeStamp tests
#################################################################################################

@pytest.mark.parametrize('timestampsDigits, expectedResult',
                         [
                             (([20, 3, 8], [20, 3, 8]), 0),
                             (([20, 3, 8], [20, 3, 18]), 10),
                             (([20, 3, 8], [21, 3, 8]), 3600)

                         ])
def test_TS_calculateTimeDiff(timestampsDigits, expectedResult):
    # arrange
    ts = Hlp.createTimestamp(timestampsDigits)

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





#################################################################################################
# ApplicationWithInstances tests
#################################################################################################
