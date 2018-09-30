#for SWALIM datasets http://frrmis.faoso.net/rivers/levels before you need to 
#1 - change column names to COLLECTIONDATE, Level and Discharge
#2 - eliminate the space (replace all = _/ --> /)
#3  - text to columns - fixed with -> date -> DMY

library(gsheet)
library(lubridate)
library(zoo)
library(rJava)
library(xlsx)
library(plyr)
library(readxl)
options(digits=5)
setwd("~/Desktop")
BW_riverlevel <- read_excel("BW_riverlevel.xlsx")
  col_types = c("date", "text", "text")

#View
(BW_riverlevel)

#rename columns
library(reshape)
BW_riverlevel <- rename(BW_riverlevel, c(COLLECTIONDATE="Date"))

#change date format and create a variable (df) of date
Date<-as.Date(BW_riverlevel$Date, "%m/%d/%y") #ignore the timezone warning
as.numeric(as.character(BW_riverlevel$Level)) #ignore the warnings
Level<-lapply(substr(BW_riverlevel$Level, 1, nchar(BW_riverlevel$Level)-1), FUN = mean)

#install XTS packages
library(xts)
#install.packages("highfrequency")
library(highfrequency)

#convert to XTS
BW_riverlevel_xts=xts(BW_riverlevel, order.by=as.POSIXct(BW_riverlevel$Date, format="%m-d%-%y"))
head(BW_riverlevel_xts) #ignore the timezone thing for now

#remove column from XTS file
BW_riverlevel_xts$Date=NULL

library(dplyr)
library (data.table)

BW_riverlevel$Date <- as.Date( as.Date(BW_riverlevel$Date), "%y-%m-%d")
BW_riverlevel[,2:ncol(BW_riverlevel)] <- sapply(BW_riverlevel[,2:ncol(BW_riverlevel)], as.character)
as.numeric(BW_riverlevel$Level)

#convert Level in XTS numeric values
Levelnumeric= data.matrix(as.data.frame(BW_riverlevel_xts))

#calculate daily to monthly average
monthlyaverage <-apply.monthly(BW_riverlevel_xts$Level, FUN = mean)

#export in excel
write.xlsx(x = monthlyaverage, file = "averagemonthly.xlsx",
           sheetName = "LevelperMonth", row.names = TRUE)

#put monthly values together 
riverlevel <- aggregate(cbind(Level)~(month(Date)+year(Date)), data=BW_riverlevel_xts$Level, means=rowMeans(Level), FUN =mean, na.rm=TRUE)
