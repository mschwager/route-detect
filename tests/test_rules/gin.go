package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()

	// ruleid: gin-route-unauthenticated
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})

	// ruleid: gin-route-authenticated
	r.GET("/ping", func(c *gin.Context) {
		Auth()
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})

	r.Run()
}

func argument(router *gin.RouterGroup) {
	// ruleid: gin-route-unauthenticated
	router.GET("/svg", func(c *gin.Context) {
		c.Data(http.StatusOK, "image/svg+xml", "data")
	})
}

func group() {
	router := gin.Default()

	v1 := router.Group("/v1")
	{
		// ruleid: gin-route-unauthenticated
		v1.GET("/ping", func(c *gin.Context) {
			c.JSON(200, gin.H{
				"message": "pong",
			})
		})
	}

	v2 := router.Group("/v2").Use(Middleware())
	{
		// ruleid: gin-route-unauthenticated
		v2.GET("/ping", func(c *gin.Context) {
			c.JSON(200, gin.H{
				"message": "pong",
			})
		})

		// ruleid: gin-route-unauthenticated
		v2.GET("/ping", handlerFn)
	}

	db := router.Group("/db").Use(authMiddleware.MiddlewareFunc())
	{
		// ruleid: gin-route-authenticated
		db.GET("/tables/page", gen.GetDBTableList)
	}

	router.Run(":8080")
}
