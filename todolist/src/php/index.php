<?php
require 'aws/aws-autoloader.php';
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


*/

$dynamodbclient = Aws\DynamoDb\DynamoDbClient::factory([
  'credentials' => [
    'key'       => $array_ini_file['aws_access_key_id'],
    'secret'    => $array_ini_file['aws_secret_access_key'],
  ],
  'region' => 'ap-northeast-1',
  'version' => 'latest',
]);

$args = array(
  'TableName' => 'table_name',
  'Key' => array(
      'field1' => array('N' => '1201'),
      'field2' => array('S' => 1),
  ),
  'ConsistentRead' => true,
);
$result = $dynamodbclient->getItem($args);

// 結果を表示
echo('<pre>');
var_dump($result);
echo('</pre>');
