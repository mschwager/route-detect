package main

import (
	"net/http"

	"github.com/auth0/go-jwt-middleware"
	"github.com/dgrijalva/jwt-go"
)

func main() {
	jwtMiddleware := jwtmiddleware.New(jwtmiddleware.Options{
		SigningMethod: jwt.SigningMethodRS256,
	})

	router := mux.NewRouter()

	// ruleid: gorilla-route-unauthenticated
	router.HandleFunc("/products", ProductsHandler)

	// ruleid: gorilla-route-unauthenticated
	router.PathPrefix("/").Handler(catchAllHandler)

	// ruleid: gorilla-route-unauthenticated
	router.PathPrefix("/static/").Handler(http.StripPrefix("/static/", http.FileServer(http.Dir(dir))))

	// ruleid: gorilla-route-unauthenticated
	router.HandleFunc("/articles/{category}/{id:[0-9]+}", ArticleHandler).Name("article")

	// ruleid: gorilla-route-unauthenticated
	router.Host("{subdomain}.example.com").
		Path("/articles/{category}/{id:[0-9]+}").
		Queries("filter", "{filter}").
		HandlerFunc(ArticleHandler).
		Name("article")

	subrouter := router.Host("www.example.com").Subrouter()

	// ruleid: gorilla-route-unauthenticated
	subrouter.HandleFunc("/products/", ProductsHandler)

	// ruleid: gorilla-route-unauthenticated
	subrouter.Path("/articles/{category}/{id:[0-9]+}").
		HandlerFunc(ArticleHandler).
		Name("article")

	// ruleid: gorilla-route-authenticated
	router.HandleFunc("/products", jwtMiddleware.Handler(ProductsHandler))

	authSubrouter := router.Host("www.example.com").Subrouter()

	authSubrouter.Use(jwtMiddleware.Handler)

	// ruleid: gorilla-route-authenticated
	authSubrouter.HandleFunc("/products/", ProductsHandler)

	unauthSubrouter := authSubrouter.Host("www.example.com").Subrouter()

	unauthSubrouter.Use(Public.Handler)

	// ruleid: gorilla-route-unauthenticated
	unauthSubrouter.HandleFunc("/products/", ProductsHandler)

	http.Handle("/", router)
}
