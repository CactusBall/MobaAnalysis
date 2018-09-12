setwd('/Users/emrys/Documents/Projects/MobaAnalysis/analysis')

library('rjson')

result <- fromJSON(file="battle_hours.json")
json_data = as.data.frame(result)
print(json_data)
print(typeof(json_data))
b <- c(result['00'][1], 
       result['01'][1], 
       result['02'][1], 
       result['03'][1], 
       result['04'][1],
       result['05'][1],
       result['06'][1],
       result['07'][1],
       result['08'][1],
       result['09'][1],
       result['10'][1],
       result['11'][1],
       result['12'][1],
       result['13'][1],
       result['14'][1],
       result['15'][1],
       result['16'][1],
       result['17'][1],
       result['18'][1],
       result['19'][1],
       result['20'][1],
       result['21'][1],
       result['22'][1],
       result['23'][1])
v <- c(1, 2, 4)
print(typeof(v))
png(file='test.png')
plot(json_data[0], type = 'o', main='Test')
dev.off()
