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

	handler := func(c *gin.Context) {
		Auth()
		c.JSON(200, gin.H{
			"message": "pong",
		})
	}

	// todoruleid: gin-route-authenticated, gin-route-unauthenticated
	r.GET("/ping", handler)

	r.Run()
}

func argument(router *gin.Engine) {
	// ruleid: gin-route-unauthenticated
	router.GET("/svg", func(c *gin.Context) {
		c.Data(http.StatusOK, "image/svg+xml", "data")
	})
}

func argument(router *gin.RouterGroup) {
	// ruleid: gin-route-unauthenticated
	router.GET("/svg", func(c *gin.Context) {
		c.Data(http.StatusOK, "image/svg+xml", "data")
	})

	v1 := router.Group("/v1").Use(authMiddleware.MiddlewareFunc())
	{
		// ruleid: gin-route-authenticated
		v1.GET("/ping", func(c *gin.Context) {
			c.JSON(200, gin.H{
				"message": "pong",
			})
		})

		// ruleid: gin-route-authenticated
		v1.GET("/ping", handlerFn)
	}
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

	v3 := v2.Group("/v3").Use(Middleware())
	{
		// ruleid: gin-route-unauthenticated
		v3.GET("/ping", func(c *gin.Context) {
			c.JSON(200, gin.H{
				"message": "pong",
			})
		})

		// ruleid: gin-route-unauthenticated
		v3.GET("/ping", handlerFn)
	}

	v4 := v3.Group("/v4").Use(Middleware())
	{
		// ruleid: gin-route-unauthenticated
		v4.GET("/ping", func(c *gin.Context) {
			c.JSON(200, gin.H{
				"message": "pong",
			})
		})

		// ruleid: gin-route-unauthenticated
		v4.GET("/ping", handlerFn)
	}

	v5 := router.Group("/v5").Use(authMiddleware.MiddlewareFunc())
	{
		// ruleid: gin-route-authenticated
		v5.GET("/ping", func(c *gin.Context) {
			c.JSON(200, gin.H{
				"message": "pong",
			})
		})

		// ruleid: gin-route-authenticated
		v5.GET("/ping", handlerFn)
	}

	v6 := v3.Group("/v6", authMiddleware.MiddlewareFunc())
	{
		// todoruleid: gin-route-authenticated, gin-route-unauthenticated
		v6.GET("/ping", func(c *gin.Context) {
			c.JSON(200, gin.H{
				"message": "pong",
			})
		})

		// todoruleid: gin-route-authenticated, gin-route-unauthenticated
		v6.GET("/ping", handlerFn)
	}

	// todoruleid: gin-route-authenticated, gin-route-unauthenticated
	router.Group("/").Use(authentication.RequireApplicationToken()).POST("/message", handlerFn)

	router.Run(":8080")
}
