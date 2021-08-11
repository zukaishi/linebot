package main

import (
	"fmt"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
)

type todolist struct {
	mid          string `json:"mid"`
	unixtime     int    `json:"unixtime"`
	todo_name    string `json:"todo_name"`
	comment      string `json:"comment"`
	start        int    `json:"start"`
	start_alarm  int    `json:"start_alarm"`
	end          int    `json:"end"`
	end_alarm    int    `json:"end_alarm"`
	routine_flag int    `json:"routine_flag"`
	delete_flag  int    `json:"delete_flag"`
}

var db = dynamodb.New(session.New(), aws.NewConfig().WithRegion("ap-northeast-1"))

func main() {
	hoge()
}

func hoge() {
	fmt.Println("Hello hoge!")
}

func getItem(isbn string) (*todolist, error) {
	input := &dynamodb.GetItemInput{
		TableName: aws.String("todolist"),
		Key: map[string]*dynamodb.AttributeValue{
			"mid": {
				S: aws.String(isbn),
			},
		},
	}

	result, err := db.GetItem(input)
	if err != nil {
		return nil, err
	}
	if result.Item == nil {
		return nil, nil
	}

	bk := new(todolist)
	err = dynamodbattribute.UnmarshalMap(result.Item, bk)
	if err != nil {
		return nil, err
	}

	return bk, nil
}
