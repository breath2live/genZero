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
ind['ma1'] = indicator.getMA(stock['close'], window=10)
ind['ma2'] = indicator.getMA(stock['close'], window=30)
ind['rank1'] = indicator.getRank(ind['ma1']-ind['ma2'], window=50)
ind['ivrank1'] = indicator.getRank(stock['iv-close'], window=50)

# create strategy
strat = strategy()
strat.setStock(stock)
#strat.setOption(option)
strat.setIndicator(ind)
strat.addCondition('option', "self.newWeek()")
strat.addCondition('option', "self.indicatorRow('ivrank1') > 50")
strat.addCondition('option', "self.indicatorRow('ma1') > self.indicatorRow('ma2')")
strat.addCondition('option', "self.stockRow('close') > self.indicatorRow('ma1')")
strat.addExecution('option', "showMe(self.metadata.name, self.date)")
strat.runDates(enddate='2020-04-01')










# end script
showMe('ending script', id)
