# Pamplona Alta Poverty Survey
# Water Access Decision Tree

library(tree)
library(dplyr)
library(randomForest)


df <- read.csv('/Users/SeanOMalley1/AnacondaProjects/SeanOMalleyCodePortfolio/Development\ Economics/PovertySurveys/df_imp.csv')

head(df)

# remove columns we don't need for prediction

df <- df %>% select(-c(DIRECCION,X,FAM_N))

# summary

summary(df)

# make agua categorical

df$agua <-  as.factor(df$agua)
df$internet <-  as.factor(df$internet)
df$banco <-  as.factor(df$banco)
df$iglesia <-  as.factor(df$iglesia)
df$dejar_hijos <-  as.factor(df$dejar_hijos)

# glimpse

glimpse(df)


################## Tree 1

# build model for prediction

df_tree_1 <- tree(agua~., data = df)

# summarize decision tree 1

summary(df_tree_1)

# plot 

plot(df_tree_1)
text(df_tree_1, pretty = 0)

# detailed summary

df_tree_1


################## Tree 2

# test and train group to test validity

set.seed(101)
train=sample(1:nrow(df), 300)

# build tree with subset train

df_tree_2 = tree(agua~., df, subset=train)

# summarize tree 2

summary(df_tree_2)

# visualize
plot(df_tree_2)
text(df_tree_2, pretty=0)


# take the train to predict a test dataset

df_tree_2_pred = predict(df_tree_2, df[-train,], type="class")

# evaluate model by printing a concusion matrix

df_tree_2_pred_res = with(df[-train,], table(df_tree_2_pred, agua))

df_tree_2_pred_res

# accuracy : not that great, we need to do some pruning to improve accuracy and interpretablity

df_tree_2_pred_acc = (df_tree_2_pred_res[1,1] + df_tree_2_pred_res[2,2]) / sum(df_tree_2_pred_res[1:2,1:2])

print(paste("Accuracy of ",df_tree_2_pred_acc*100,"%", sep = ""))

# prune with cross validation

pruned_df_tree_2 = prune.misclass(df_tree_2, best = 4)

summary(pruned_df_tree_2)

plot(pruned_df_tree_2)
text(pruned_df_tree_2, pretty=0)

# test pruned tree

pruned_df_tree_2_pred = predict(pruned_df_tree_2, df[-train,], type="class")

# evaluate model by printing a concusion matrix

pruned_df_tree_2_res = with(df[-train,], table(pruned_df_tree_2_pred, agua))

pruned_df_tree_2_res

# accuracy 

pruned_df_tree_2_acc = (pruned_df_tree_2_res[1,1] + pruned_df_tree_2_res[2,2]) / sum(pruned_df_tree_2_res[1:2,1:2])

print(paste("Accuracy of ",pruned_df_tree_2_acc*100,"%", sep = ""))

# pretty

#fancyRpartPlot(pruned_df_tree_2)


################ Tree With RPart

library(rpart)

# grow tree 
rpart_tree <- rpart(agua ~ ., data=df, method="class", maxdepth = 4)

printcp(rpart_tree) # display the results 
plotcp(rpart_tree) # visualize cross-validation results 
summary(rpart_tree) # detailed summary of splits

# plot tree 
plot(rpart_tree, uniform=TRUE, main="Classification Tree for Water Access")
text(rpart_tree, use.n=TRUE, all=TRUE, cex=.8)

#install.packages('rattle')
#install.packages('rpart.plot')
#install.packages('RColorBrewer')
library(rattle)
library(rpart.plot)
library(RColorBrewer)

# plot nicely 

fancyRpartPlot(rpart_tree)



