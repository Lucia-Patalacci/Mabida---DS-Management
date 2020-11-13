# SUPERVISED LEARNING #

rm( list=ls() )

### Step 1. Load the data. ##########################
library(readr)
library(dplyr)
library(tidyverse)
library(reshape2)
library(caret)
library(ranger)
library(e1071)

setwd("~/Documents")
housing = read.csv('housing.csv')

#a) Take a look at the data
head(housing)

#b) Check which variables are numeric/categorical
str(housing)
colnames(housing)
###trimming white spaces in ocean_proximity levels 
housing$ocean_proximity <- str_replace (housing$ocean_proximity, " ", "")

###10 variables of which feature "ocean_proximity is a categorical with 5 levels. The other 9 features are numericals.

#c) Plot variables histogram

library(psych)
##Viewing variables histograms on diagonal and correlation between pairs of variables (graphical and numerical)###

pairs.panels(housing[c("housing_median_age", "total_rooms","total_bedrooms","population","households","median_income","median_house_value")]
        ,main="Scatterplot Matrix")

###from scatterplot we notice an approximating "normal" curve for "housing_median_age" distribution but it presents two modes values
###variables "median_house_value" and "median_income" have both a quite "normal " curve with a left skewness.
###features "total_bedroom", "total_rooms" with "population" are highly correlated (as expected) and "population"is also correlated with "households"


### Step 2. Data Cleaning ############################

#a)Impute missing values: Fill median for the only column with missing values. Why do we use the median? 

###In summary, it can notice NA's presence in "total_bedrooms" feature###
### we substitute NA's with median as the intermediate value in the distribution not influenced by extreme values###

housing$total_bedrooms[is.na(housing$total_bedrooms)] <- median(housing$total_bedrooms, na.rm = TRUE)
        
#b) Create new variables
# Fix the total columns making them means
mean_rooms<-(housing[,4])/housing$population
mean_bedrooms<-(housing[,5])/housing$population

# Drop original total columns
housing1<-housing[,-c(4:5)]
housingdef<-cbind(housing1,mean_rooms,mean_bedrooms)
colnames(housingdef)

pairs.panels(housingdef[c("housing_median_age","mean_rooms","mean_bedrooms","population","households","median_income","median_house_value")]
             ,main="Scatterplot Matrix2")

####"mean_rooms"and "mean_bedrooms" variables frequency histogram and don't change, correlation decreases from 0.93 to 0.85 but they become quite 
####  uncorrelated with "population" feature

#c) Turn categoricals into booleans
#-Get a list of all the categories in the 'ocean_proximity' column
table (housingdef$ocean_proximity) #### 5 levels


#-Make a new empty dataframe of all 0s, where each category is its own colum
#-Use a for loop to populate the appropriate columns of the dataframe
#-Drop the original column from the dataframe.

#d) Scale the numerical variables (do not scale 'median_house_value', it will be the target variable)
#e)Merge the altered numerical and categorical dataframes

preprocessParams <- preProcess(x=housingdef, method=c("center", "scale"))
# summarize transform parameters
print(preprocessParams)
# transform the dataset using the parameters
head(housingdef <- predict(preprocessParams, housingdef))

dummies <- dummyVars("~ .", data = housingdef, sep = "_")
head(predict(dummies, newdata=housingdef))

# give a glance and summarize the transformed dataset
summary(housingdef)
        
 ### Step 3. Create a test set ################

set.seed(998)
inTraining <- createDataPartition(housing$median_house_value, p = .75, list = FALSE)
house_train <- housing[ inTraining,]
house_test  <- housing[-inTraining,]
head(house_train)
        
### Step 4. Test predictive models. #############
 #a) Start using a simple linear model using 3 of the avaliable predictors. Median income, total rooms and population. 
library('boot')
glm_house = glm(median_house_value~median_income+total_rooms+population,family="gaussian", data=house_train)

summary(glm_house)
#summary explain that all the three predictive variables are significant to explain target "median house value" (Pr(>|t|) <0.05, so we reject 
#Hypothesis that target is non influenced by features "median_income"+"total_rooms"+"population"

#let'observe residuals of model
#verify residual of multivariate linear model
par(mfrow=c(2,2))
plot(glm_house)
###Residual vs predicted values plot explains linear relationship. Residuals however are not quite normally distributed
### third plot shows that residuals are randomly spread and the red line is fairly plate.
###Fourth plot shows that there aren't cases of influential outiliers (see obs n. 15361 just close to Cook's distance upper range)

#b)Do cross validation (K=5) to test the model using the training data.
#What does K=5 mean?
###K is yhe number of groups into which the data should be split to estimate the cross-validation prediction error.

# check "delta" value after cross validation

cv.glm_house=cv.glm(data=house_train, glm_house, K=5)
str(cv.glm_house)

# The first component of delta is the raw cross-validation estimate of prediction error.
delta_house<-cv.glm_house$delta[1]
        
#c) Compute Root Mean Square Error using "delta" value
library(gbm)
glm_cv_rmse <- sqrt(delta_house)
        
#d) Use Random forest model and check variables importance. Which are the most important variables?
library(MASS)
library(randomForest)
housingRF <- model.matrix( 
  ~ housing_median_age  + median_income  + total_rooms + ocean_proximity+median_house_value,data=house_train
)
housing.rf<-randomForest(median_house_value~ . , data = house_train, ntree=1000, importance=T,proximity = T)
print(housing.rf)
plot(housing.rf,xlim=c(1,1000))

#most important variables 
importance(housing.rf)
#varImp(housing.rf)
#the first column is the mean increase in actual StandarError  and the second the difference between
###Residuals Sum of Squares before and after the split (the mean increase in node impurity)
#graphically:
varImpPlot(housing.rf)
###highest contribution in terms of MSE comes from "median_income" followed by "ocean_proximity" and "housing_median_age"
####that means, tne "median_house_value" is most influenced by income, proximity to the ocean and house age.

#e) How well does the model predict on the test data? Compute Root Mean Square Error as sqrt( mean(((y_pred - test_y)^2)) )

 # Use the model to predict the evaluation.
y_pred <- predict(housing.rf, newdata=house_test)
test_y<-house_test$median_house_value
RMSE_housing.rf<-sqrt(mean(((y_pred - test_y)^2)))

###we notice that RMSE of Random Forest Model is considerably lower than RMSE of linear model.

 ### Step 5. ##########################################
 #a) Suggestions on ways to improve the results
### #linear regression with normalized predictors and stepwise BIC selection of parameter 
n<-nrow(house_train)
house0_norm <- lm(median_house_value~1,data=house_train)
house1_norm <- lm(median_house_value~.,data=house_train)
house_lin_bic <- stepAIC(house1_norm,scope=list(lower=house0_norm,upper=house1_norm),direction="both",k=log(n),trace=F)
summary(house_lin_bic)
pred_lin_bic <- predict(house_lin_bic,house_test)
RMSE_lin_house<-sqrt(mean(((pred_lin_bic - house_test$median_house_value)^2)))
#### in this case the best model is the one with all 9 parameters but the Rsquared is only 0.6479
####RMSE value is still higher than RMSE of RF model

#b) try some other models to see if they improve Root Mean Square Error: gradient boosting - library(gbm),
#extreme gradient boosting - library(xgb), support vevtor machines - library(e1071),
 #neural networks - library(neuralnet)

####support vector machines####
svm_house = svm(median_house_value~.,data=house_train, kernel = "linear", cost = 10, scale = FALSE)
print(svm_house)
predictedY <- predict(svm_house, house_test)
#points(house_test$median_house_value, predictedY, col = "red", pch=4)
RMSE_svm_house<-sqrt(mean(((predictedY - house_test$median_house_value)^2)))
#RMSE in this case is higher than one get with Random Forest models

####neural networks####
library(neuralnet)
#fit neural network
set.seed(1234)
housingNN <- model.matrix( 
 ~ housing_median_age  + median_income  + total_rooms + ocean_proximity+ population+ median_house_value,data=house_train
)
head(housingNN)
NN = neuralnet(median_house_value ~ housing_median_age  + median_income  + total_rooms + ocean_proximityINLAND+
                 ocean_proximityISLAND+ ocean_proximityNEARBAY+ ocean_proximityNEAROCEAN + population,
               data=housingNN, hidden = c(5,3) , linear.output = T,stepmax = 1e7)

# plot neural network
plot(NN)
print(NN$median_house_value)

## Prediction using neural network
predict_testNN = compute(NN,housingNN[,1:8])
predict_testNN = predict_testNN$median_house_value

#plot(predict_testNN$median_house_value, predict_testNN, col='blue', pch=16, ylab = "predicted rating NN", xlab = "real rating")
#abline(0,1)

# Calculate Root Mean Square Error (RMSE)
RMSE.NN = sqrt(((predict_testNN$median_house_value - predict_testNN)^2))


######################my notes######################
#set.seed(101)
#x <- housingdef[ sample(1:nrow(housingdef), nrow(housingdef), replace = F),]
#train_x <- housingdef[ 1:floor(nrow(x)*.75),]
#test_x <- housingdef[ (floor(nrow(x)*.75)+1):nrow(x),]
#test_y<-test_x$median_house_value

#set.seed(2)
#housingNN <- model.matrix( 
#  ~ median_house_value+ housing_median_age  + median_income  + mean_rooms + ocean_proximity,data=house_train1
#)