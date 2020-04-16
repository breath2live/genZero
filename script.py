# import
from strategy import strategy
import indicator

# start script
showMe('starting script', id)

# load bigdata
if stock is None: loadstock()
#if option is None: loadoption()

# build indicator
ind = pd.DataFrame([], index=pd.DatetimeIndex(stock.index))
ind['ma1'] = indicator.getMA(stock['close'], window=20)
ind['ma2'] = indicator.getMA(stock['close'], window=50)
ind['rank1'] = indicator.getRank(ind['ma1']-ind['ma2'], window=50)
ind['ivrank1'] = indicator.getRank(stock['iv-close'], window=50)

# create strategy
strat = strategy()
strat.setStock(stock)
#strat.setOption(option)
strat.setIndicator(ind)
strat.addTrigger('date', "self.newWeek()")
strat.addTrigger('ivrank', "self.indicatorRow('ivrank1') > 50")
strat.addTrigger('direction', "self.indicatorRow('ma1') > self.indicatorRow('ma2')")
strat.addExecution('info', "showMe(self.metadata.name, self.date)")
strat.runDates(enddate='2020-04-01')










# end script
showMe('ending script', id)
