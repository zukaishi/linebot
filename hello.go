package main

import (
	"fmt"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

func linebot(request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {

	fmt.Println("*** body")
	fmt.Println(request)
	fmt.Println(request.Body)
	fmt.Println("*** body")

	return events.APIGatewayProxyResponse{Body: request.Body, StatusCode: 200}, nil
}

func main() {
	lambda.Start(linebot)
}
