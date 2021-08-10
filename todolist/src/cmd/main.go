package main

import (
	"fmt"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
)

var db = dynamodb.New(session.New(), aws.NewConfig().WithRegion("ap-northeast-1"))

func main() {
	hoge()
	fuga()
}

func hoge() {
	fmt.Println("Hello hoge!")
}

func fuga() {
	fmt.Println("Hello fuga!")
}
