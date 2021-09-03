# TODOLIST

## 画面イメージ
![Untitled](https://user-images.githubusercontent.com/22611735/126231053-ef22a400-8a6a-4236-89c0-fbe5bc5bec66.jpg)

## DB
todolist
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
![todolist](https://user-images.githubusercontent.com/22611735/128646914-c92323bf-c7e2-48bd-9c51-cfd886c86ff9.jpg)

## AWS
- CloudFormation
- CodePipline
- DynamoDB
- API Gateway
- Lambda
- S3 

## 言語
- PHP (server less php）

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

## SAMインストール
```
$ brew tap aws/tap
$ brew install aws-sam-cli
```

```
Error: 
  homebrew-core is a shallow clone.
To `brew update`, first run:
  git -C /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core fetch --unshallow
This command may take a few minutes to run due to the large size of the repository.
This restriction has been made on GitHub's request because updating shallow
clones is an extremely expensive operation due to the tree layout and traffic of
Homebrew/homebrew-core and Homebrew/homebrew-cask. We don't do this for you
automatically to avoid repeatedly performing an expensive unshallow operation in
CI systems (which should instead be fixed to not use shallow clones). Sorry for
the inconvenience!
==> Searching for similarly named formulae...
Error: No similarly named formulae found.
Error: No available formula or cask with the name "aws-sam-cli".
==> Searching for a previously deleted formula (in the last month)...
Warning: homebrew/core is shallow clone. To get its complete history, run:
  git -C "$(brew --repo homebrew/core)" fetch --unshallow

Error: No previously deleted formula found.
==> Searching taps on GitHub...
Error: No formulae found in taps.
```

```
$ brew update
```

```
Error: 
  homebrew-core is a shallow clone.
To `brew update`, first run:
  git -C /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core fetch --unshallow
This command may take a few minutes to run due to the large size of the repository.
This restriction has been made on GitHub's request because updating shallow
clones is an extremely expensive operation due to the tree layout and traffic of
Homebrew/homebrew-core and Homebrew/homebrew-cask. We don't do this for you
automatically to avoid repeatedly performing an expensive unshallow operation in
CI systems (which should instead be fixed to not use shallow clones). Sorry for
the inconvenience!
```
```
$ git -C /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core fetch --unshallow
```
```
remote: Enumerating objects: 710787, done.
remote: Counting objects: 100% (710732/710732), done.
remote: Compressing objects: 100% (242323/242323), done.
remote: Total 700959 (delta 465819), reused 690713 (delta 455771), pack-reused 0
Receiving objects: 100% (700959/700959), 257.94 MiB | 4.34 MiB/s, done.
Resolving deltas: 100% (465819/465819), completed with 8215 local objects.
From https://github.com/Homebrew/homebrew-core
   c75ce10e8f1..1f30689d7e3 master     -> origin/master
```

```
$ brew update
$ brew install aws-sam-cli
```
```
Error: python@3.8: the bottle needs the Apple Command Line Tools to be installed.
  You can install them, if desired, with:
    xcode-select --install
```

```
$ xcode-select --install
- install log
$ brew install aws-sam-cli
```

```
$ sam --version
SAM CLI, version 1.29.0
```

<img width="474" alt="スクリーンショット 2021-08-19 6 56 30" src="https://user-images.githubusercontent.com/22611735/129977568-44f28bf5-72e7-4c49-ae1c-5ab6b209ff0c.png">


## CD
- CodePipeline
- lambdaへtodolist、todoadd、toodupd、tododel関数作成
```
sam package --template-file template.yaml  --output-template-file package.yaml          --s3-bucket todolist-phpserverless-zukaishi
sam deploy --template-file package.yaml --stack-name todolist-phpserverless-zukaishi --capabilities CAPABILITY_IAM
```

## dynamodb書き込み
```
"__type":"com.amazon.coral.service#AccessDeniedException","Message":"User: arn:aws:iam::431928468872:user/aws-teraform- (truncated...)
 AccessDeniedException (client): User: arn:aws:iam::431928468872:user/aws-teraform-s3 is not authorized to perform: dynamodb:PutItem on resource: arn:aws:dynamodb:ap-northeast-1:431928468872:table/todolist - {"__type":"com.amazon.coral.service#AccessDeniedException","Message":"User: arn:aws:iam::431928468872:user/aws-teraform-s3 is not authorized to perform: dynamodb:PutItem on resource: arn:aws:dynamodb:ap-northeast-1:431928468872:table/todolist"}
 ```
 credentials.ini　指定を間違えていたため修正
 
```
{"__type":"com.amazon.coral.validate#ValidationException","message":"One or more parameter values were invalid: Type mis (truncated...)
 ValidationException (client): One or more parameter values were invalid: Type mismatch for key unixtime expected: N actual: S - {"__type":"com.amazon.coral.validate#ValidationException","message":"One or more parameter values were invalid: Type mismatch for key unixtime expected: N actual: S"}
```
カラム名と値が間違えていたため修正
```
Aws\Result Object
(
    [data:Aws\Result:private] => Array
        (
            [@metadata] => Array
                (
                    [statusCode] => 200
                    [effectiveUri] => https://dynamodb.ap-northeast-1.amazonaws.com
                    [headers] => Array
                        (
                            [server] => Server
                            [date] => Mon, 30 Aug 2021 21:47:42 GMT
                            [content-type] => application/x-amz-json-1.0
                            [content-length] => 2
                            [connection] => keep-alive
                            [x-amzn-requestid] => 7JL9N7KLO6JPPUB5DSDS0BU2IVVV4KQNSO5AEMVJF66Q9ASUAAJG
                            [x-amz-crc32] => 2745614147
                        )

                    [transferStats] => Array
                        (
                            [http] => Array
                                (
                                    [0] => Array
                                        (
                                        )

                                )

                        )

                )

        )

    [monitoringEvents:Aws\Result:private] => Array
        (
        )

)
```

getitem
```
Fatal error: Uncaught InvalidArgumentException: Found 1 error while validating the input provided for the GetItem operation:
[Key] is missing and is a required parameter in /Users/hishizuka/Work/git/linebot/todolist/src/php/aws/Aws/Api/Validator.php:65
Stack trace:
#0 /Users/hishizuka/Work/git/linebot/todolist/src/php/aws/Aws/Middleware.php(78): Aws\Api\Validator->validate('GetItem', Object(Aws\Api\StructureShape), Array)
#1 /Users/hishizuka/Work/git/linebot/todolist/src/php/aws/Aws/IdempotencyTokenMiddleware.php(77): Aws\Middleware::Aws\{closure}(Object(Aws\Command), NULL)
#2 /Users/hishizuka/Work/git/linebot/todolist/src/php/aws/Aws/AwsClientTrait.php(64): Aws\IdempotencyTokenMiddleware->__invoke(Object(Aws\Command))
#3 /Users/hishizuka/Work/git/linebot/todolist/src/php/aws/Aws/AwsClientTrait.php(58): Aws\AwsClient->executeAsync(Object(Aws\Command))
#4 /Users/hishizuka/Work/git/linebot/todolist/src/php/aws/Aws/AwsClientTrait.php(86): Aws\AwsClient->execute(Object(Aws\Command))
#5 /Users/hishizuka/Work/git/linebot/todoli in /Users/hishizuka/Work/git/linebot/todolist/src/php/aws/Aws/Api/Validator.php on line 65
```
ここでまた躓く

```
 $params = [
    'ConsistentRead' => true,
    'TableName' => 'todolist',
    'Key' => $item
  ];
```
Key が Itemになっていたためだった

LINE Bot作成
