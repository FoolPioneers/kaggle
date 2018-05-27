# Description for competition of Homecredit

## Background
Many people struggle to get loans due to insufficient or non-existent credit histories. And, unfortunately, this population is often taken advantage of by untrustworthy lenders.

Home Credit strives to broaden financial inclusion for the unbanked population by providing a positive and safe borrowing experience. In order to make sure this underserved population has a positive loan experience, Home Credit makes use of a variety of alternative data--including telco and transactional information--to predict their clients' repayment abilities.

While Home Credit is currently using various statistical and machine learning methods to make these predictions, they're challenging Kagglers to help them unlock the full potential of their data. Doing so will ensure that clients capable of repayment are not rejected and that loans are given with a principal, maturity, and repayment calendar that will empower their clients to be successful.

## Evaluation
Submissions are evaluated on area under the ROC curve between the predicted probability and the observed target.

### Submission File
For each SK_ID_CURR in the test set, you must predict a probability for the TARGET variable. The file should contain a header and have the following format:

```
SK_ID_CURR,TARGET  
100001,0.1  
100005,0.9  
100013,0.2  
etc.
```

## Data Description
+ application_{train|test}.csv

	 + This is the main table, broken into two files for Train (with TARGET) and Test (without TARGET).
	+ Static data for all applications. One row represents one loan in our data sample.  

* bureau.csv

	+ All client's previous credits provided by other financial institutions that were reported to Credit Bureau (for clients who have a loan in our sample).
	+ For every loan in our sample, there are as many rows as number of credits the client had in Credit Bureau before the application date.

+ bureau_balance.csv

	+ Monthly balances of previous credits in Credit Bureau.
This table has one row for each month of history of every previous credit reported to Credit Bureau – i.e the table has (#loans in sample * # of relative previous credits * # of months where we have some history observable for the previous credits) rows.

+ POS\_CASH_balance.csv

	+ Monthly balance snapshots of previous POS (point of sales) and cash loans that the applicant had with Home Credit.
	+ This table has one row for each month of history of every previous credit in Home Credit (consumer credit and cash loans) related to loans in our sample – i.e. the table has (#loans in sample * # of relative previous credits * # of months in which we have some history observable for the previous credits) rows.

+ credit\_card_balance.csv

	+ Monthly balance snapshots of previous credit cards that the applicant has with Home Credit.
	+ This table has one row for each month of history of every previous credit in Home Credit (consumer credit and cash loans) related to loans in our sample – i.e. the table has (#loans in sample * # of relative previous credit cards * # of months where we have some history observable for the previous credit card) rows.

+ previous_application.csv

	+ All previous applications for Home Credit loans of clients who have loans in our sample.
	+ There is one row for each previous application related to loans in our data sample.

+ installments\_payments.csv

	+ Repayment history for the previously disbursed credits in Home Credit related to the loans in our sample.
There is a) one row for every payment that was made plus b) one row each for missed payment.
	+ One row is equivalent to one payment of one installment OR one installment corresponding to one payment of one previous Home Credit credit related to loans in our sample.

+ HomeCredit\_columns_description.csv

	+ This file contains descriptions for the columns in the various data files.

![image](https://storage.googleapis.com/kaggle-media/competitions/home-credit/home_credit.png)

## 目录说明
项目目录如下：

```
├── code
├── data
│   ├── POS_CASH_balance.csv
│   ├── application_test.csv
│   ├── application_train.csv
│   ├── bureau.csv
│   ├── bureau_balance.csv
│   ├── credit_card_balance.csv
│   ├── installments_payments.csv
│   └── previous_application.csv
├── long.li
├── material
│   ├── HomeCredit_columns_description.csv
│   └── vardemo
│       ├── configpy
│       │   ├── __pycache__
│       │   │   ├── demo_filter_func.cpython-35.pyc
│       │   │   └── demo_varname.cpython-35.pyc
│       │   ├── demo_filter_func.py
│       │   └── demo_varname.py
│       ├── demo_main_test.py
│       ├── demo_metafunc
│       │   ├── demo_metafunc_test.py
│       │   ├── demo_varname.txt
│       │   ├── dictexp.txt
│       │   └── gen_varname.R
│       ├── dict_base_test.py
│       └── test
│           └── basic_test_data.txt
├── model
├── readme.md
└── submit
    └── sample_submission.csv
```
1. code 目录下放置公用的数据处理代码；
2. data放置数据，现在全部都是捷信提供的数据，后续的处理以后的变量也置于这个目录下。code目录下的变量处理程序输出目录最好是data目录，这样其他人可以在自己的电脑上生成变量数据和模型数据。因为这个数据量比较大，大家还是各自下载对应的数据，只上传处理代码就好。数据的下载地址为[Home Credit Default Risk](https://www.kaggle.com/c/home-credit-default-risk/data)；
3. long.li个人代码目录，在一级目录下可以建自己的个人代码，因为每个人都可能搭建自己的模型，可以在自己的目录下训练，最后能导出来就行；
4. material目录，存放一些参考资料，现在是字段的说明文件和Python版的变量代码参考文件
5. model 最终模型存放目录,所有文件以个人代号开头，如loveletter，panda，gavin...

## 任务项
从项目提供的数据来看，捷信提供的数据包含两个部分，一个是外部的征信数据，以及内部的历史借款数据，以及当前这比借款的数据。内部的借款数据分为分期数据和信用卡数据，这些数据都包含明细数据，需要做相应的数据处理。所以，需要做的事情

+ 变量构造
	+ 征信数据
	+ 信用卡数据
	+ 分期数据
	+ 现金分期数据

+ 模型训练
	+ 每个人单独训练模型
	+ 不同模型方法训练模型
+ 模型融合
	+ 最终输出可以融合每个人所有的模型输出结果，所以需要有一个模型融合的部分

### 关于规范
+ 训练好的模型都放在model目录下；
+ 样本数据都从data目录读取；
+ 每个人的模型都使用同意的入口函数main， R可以使用代号前缀+main来作为入口函数；
+ 模型输出为一个或多个分数，为了保证模型融合标准化，预测分数都转为log(p/(1-p))的形式；
+ 模型分的命名都以名称代号起头，避免重名;

## 数据描述更新
+ application_{train|test}.csv
	+ 申请表单表，含客户填写信息以及外部查询汇总信息 	
+ bureau.csv
	+ 外部征信明细表，需要确定一个申请是否存在多条记录+ bureau_balance.csv
	+ 关联bureau.csv， 每月账户状态表
+ POS\_CASH_balance.csv
	+ 现金贷每月账户状态表+ credit\_card_balance.csv
	+ 循环账户每月账户状态表
+ previous\_application.csv
	+ 历史捷信内部申请信息表+ installments_payments.csv
	+ 分析还款计划表

## 会议记录
### 2018.05.22
#### 议题
+ 审批还款流程说明
+ 数据表结构讨论
+ 分工及计划

#### 分工及计划
+ EDA（本周结束）
	+ Daisy ：application_{train|test}.csv
	+ Panda：POS\_CASH\_balance.csv, installments_payments.csv
	+ Gavin: bureau.csv, bureau_balance.csv
	+ loveletter: credit\_card\_balance.csv, installments_payments.csv
	+ 鸡腿堡: previous\_application.csv
+ 周末会议议题
	+ 变量设计讨论
	+ 变量构造分工及形式确认
	+ 模型方法确认
	+ 代码规范及目录规范确认

#### 注意事项
+ EDA在标准汇总统计的基础上，还需补充子表与主表之间的对应关系
+ 变量构造可以参考之前的文档，最好有新的变量构造方法