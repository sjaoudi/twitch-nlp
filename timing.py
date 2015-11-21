class TimingFuncs(object):

    def appendTdelta(self, tdelta, tdeltas, tdeltasCapacity):
        if len(tdeltas) < tdeltasCapacity:
            tdeltas.append(tdelta)
        else:
            tdeltas.rotate()
            tdeltas[0] = tdelta

    def calcAvgTdelta(self, tdeltas):
        sum = 0
        for tdelta in tdeltas:
            sum += tdelta.microseconds

        avgTdelta = sum/len(tdeltas)
        return avgTdelta
