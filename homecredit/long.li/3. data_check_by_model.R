require(data.table)
require(gbm)
require(pROC)
require(xgboost)

df <- fread("data/application_train.csv", nrows = 100000)

varscat <- names(df)[sapply(df, class) == "character"]
varsrm <- c("SK_ID_CURR")
df4model <- df[, setdiff(names(df), c(varsrm, varscat)), with = FALSE]

ds4xgb <- as.matrix(df4model[, setdiff(names(df4model), c("TARGET")), with = FALSE])
ds4xgb <- xgb.DMatrix(ds4xgb, label = df4model$TARGET)

table(df4model$TARGET)

model <- xgb.cv(list(objective = 'binary:logistic', max_depth = 3, eta = 0.01)
                ,data = ds4xgb, nrounds = 1000, nfold = 5, metrics = "auc", early_stopping_rounds = 20)