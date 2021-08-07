# TODOLIST

## 画面イメージ
![Untitled](https://user-images.githubusercontent.com/22611735/126231053-ef22a400-8a6a-4236-89c0-fbe5bc5bec66.jpg)

## DB
todo_table
- mid [p]
- unixtime [p]
- todo_name
- comment
- start
- start_alarm
- end
- end_alarm
- routine_flag
- delete_flag

## アーキテクト

## AWS
- CloudFormation
- DynamoDB
- API Gateway
- Lambda

## LINE Bot
- LINE Bot Designer.appダウンロード
- <img width="520" alt="スクリーンショット 2021-07-21 6 09 25" src="https://user-images.githubusercontent.com/22611735/126395763-47ed2917-ff86-416a-83b4-997cbd1338e6.png">
- https://developers.line.biz/console/　アクセス後ログイン
- プロバイダの作成

## cloudformation
```
$ aws cloudformation create-stack --stack-name stack-$(date +%s) --template-body file://cloud_formation_dynamodb.yaml
```

## api swagger
- https://zukaishi.github.io/linebot/todolist/docs/dist/

## CD
- CodePipeline
- lambdaへtodolist、todoadd、toodupd、tododel関数作成

