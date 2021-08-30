<?php
require 'aws/aws-autoloader.php';
use Aws\DynamoDb\Exception\DynamoDbException;
use Aws\DynamoDb\Marshaler;
$array_ini_file = parse_ini_file('credentials.ini', true);

// S3Clientインスタンスの作成
/*
$s3client = Aws\S3\S3Client::factory([
    'credentials' => [
        'key'       => $array_ini_file['aws_access_key_id'],
        'secret'    => $array_ini_file['aws_secret_access_key'],
    ],
    'region' => 'ap-northeast-1',
    'version' => 'latest',
]);

// ローカルにファイル作成
$file    = date('YmdHis') . '.txt';
$content = <<< EOF
hoge
ふが
EOF;
file_put_contents($file, $content);

// S3にアップロード
$result = $s3client->putObject([
    'ACL'           => 'public-read',   // ACLを指定する場合、ブロックパブリックアクセスはすべてオフにする
    'Bucket'        => $array_ini_file['aws_bucket_name'],
    'Key'           => 'test.txt',
    'SourceFile'    => $file,
    'ContentType'   => mime_content_type($file),
]);
print_r($result);
*/

$dynamodbclient = Aws\DynamoDb\DynamoDbClient::factory([
  'credentials' => [
    'key'       => $array_ini_file['aws_access_key_id'],
    'secret'    => $array_ini_file['aws_secret_access_key'],
  ],
  'region' => 'ap-northeast-1',
  'version' => 'latest',
]);
$marshaler = new Marshaler();
$item = $marshaler->marshalJson('
    {
        "mid": "mid",
        "unixtime": 1,
        "todo_name": "todo_name",
        "comment": "comment",
        "start": 1,
        "start_alarm": 1,
        "end": 1,
        "end_alarm": 1,
        "routine_flag": 1,
        "delete_flag": 1
    }
');
$params = [
    'TableName' => 'todolist',
    'Item' => $item
];

try {
    $result = $dynamodbclient->putItem($params);
    print_r($result);
} catch (DynamoDbException $e) {
    echo "Unable to add item:\n";
    echo $e->getMessage() . "\n";
}