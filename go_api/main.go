package main

import (
	"bytes"
	"encoding/json"
	"io"
	"net/http"

	"github.com/gin-gonic/gin"
)

type IncomingRequest struct {
	Age           int     `json:"age"`
	Gender        string  `json:"gender"`
	HasHouse      string  `json:"has_house"`
	MaritalStatus string  `json:"marital_status"`
	Income        float64 `json:"income"`
}

type PyServerRequest struct {
	Age           int     `json:"age"`
	Gender        string  `json:"gender"`
	HasHouse      string  `json:"has_house"`
	MaritalStatus string  `json:"marital_status"`
	Income        float64 `json:"income"`
}

func predict(c *gin.Context) {
	var in IncomingRequest
	if err := c.ShouldBindJSON(&in); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid json" + err.Error()})
		return
	}
	out := PyServerRequest{
		Age:           in.Age,
		Gender:        in.Gender,
		HasHouse:      in.HasHouse,
		MaritalStatus: in.MaritalStatus,
		Income:        in.Income,
	}
	body, err := json.Marshal(out)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "marshal error: " + err.Error()})
		return
	}
	resp, err := http.Post("http://localhost:8000/predict", "application/json", bytes.NewReader(body))
	if err != nil {
		c.JSON(http.StatusBadGateway, gin.H{"error": "Failed to contact Python server"})
		return
	}
	defer resp.Body.Close()

	for k, v := range resp.Header {
		if len(v) > 0 {
			c.Header(k, v[0])
		}
	}
	c.Status(resp.StatusCode)
	_, _ = io.Copy(c.Writer, resp.Body)
}

func main() {
	router := gin.Default()
	router.POST("/go_api/predict", predict)
	err := router.Run("localhost:9090")

	if err != nil {
		return
	}
}
