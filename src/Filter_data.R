
rm(list = ls())
library(data.table)
library(openxlsx)
library(dplyr)
# setwd("/Users/nana/PycharmProjects/Cattle_and_Climate/data/")

raw.data <- read.csv("example_climate_disease.csv")
data <- subset(raw.data, select = -c(mno,district,popsize,date,farm.type,year,rate,id))

#Plot the correlation analysis between top10 variables and count
sub.data <- data[,c("count","Tgrassmin_Jul","Raindays_Dec","Frost_Apr","Tsd_Feb","RH_Dec",
                    "Tgrassmin_May","Chill_Apr","Sun_Feb","Rad_Aug","Raindays_May")]
corr <- cor(sub.data)
library(corrplot)
pdf('../img/corrplot.pdf',height = 8, width = 8)
corrplot(corr,type="upper")
dev.off()


# rm(list = ls())
library(data.table)
library(openxlsx)
library(dplyr)
setwd("/Users/nana/PycharmProjects/Cattle_and_Climate/data/")

raw.data <- read.csv("example_climate_disease.csv")
data <- subset(raw.data, select = -c(mno,district,popsize,date,farm.type,year,rate,id))

# 0:zero
# 0-5 :low
# 5-10:mid
# 10-20:high

# Discrete data
for (i in colnames(data)) {
  if (i%in% c("count")){
    data[, i] <- ifelse(data[, i]== 0,"zero",
                        ifelse(data[, i]< 5,"low_count",
                               ifelse(data[, i]< 10,"mid_count","high_count")))
  }else{
    cname1 <- paste(i,"_high",sep="")
    cname2 <- paste(i,"_low",sep="")
    data[, i] <- ifelse(data[, i] ==0,"",
                        ifelse(data[, i] >  median(data[, i]) , cname1 , cname2))
  }
}

#Filtering the strongly correlated variables
corr.data <- read.csv("corr_result.csv")
sub.corr.data <- subset(corr.data, abs(count) > 0.17)
top.feas <- sub.corr.data$X #35
new.data <- data[,top.feas]
file <- paste("data_proced.csv",sep="")
write.csv(new.data,file,row.names = FALSE)

