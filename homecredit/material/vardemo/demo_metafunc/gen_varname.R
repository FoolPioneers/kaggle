require(caret)

cat1 <- c('a', 'b','c', 'd')
cat2 <- c('p', 'q', 'm', 'n')
cat3 <- c('p', 'q', 'm', 'n')
cat4 <- c('p', 'q', 'm', 'n')
prefix <- 'n'
# m=max, s=sum, a=avg, v=var
calm <- c('m', 's', 'a', 'v')
# o=obj1, p=obj2
calObj <- c('o', 'p')


res = expand.grid(cat1, cat2, cat3, cat4, calm, calObj)

dfvar <- as.data.frame(lapply(res, as.character),stringsAsFactors = FALSE)

names(dfvar) <- c('cat1', 'cat2','cat3','cat4', 'calm', 'calObj')

dfvar <- dfvar[, c('calm', 'calObj', 'cat1', 'cat2','cat3','cat4')]

varName <- apply(dfvar,MARGIN = 1,  paste0, collapse = '')

resStr = paste(sprintf('"%s_%s"',prefix, varName), collapse = '\n,')

cat(sprintf('[%s]', resStr), file = 'demo_varname.txt')


length(unique(varName))


