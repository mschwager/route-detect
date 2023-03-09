package main

import (
	"fmt"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/jwtauth/v5"
	"github.com/go-chi/oauth"
)

func main() {
	r := chi.NewRouter()

	// ruleid: chi-route-unauthenticated
	r.Get("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("hi"))
	})

	r.Route("/articles", func(r chi.Router) {
		// ruleid: chi-route-unauthenticated
		r.With(paginate).Get("/", listArticles)

		// ruleid: chi-route-unauthenticated
		r.Post("/", createArticle)

		r.Route("/{articleID}", func(r chi.Router) {
			r.Use(ArticleCtx)
			// ruleid: chi-route-unauthenticated
			r.Put("/", updateArticle)
		})
	})

	r.Mount("/admin", adminRouter())

	http.ListenAndServe(":3333", r)
}

func router() http.Handler {
	r := chi.NewRouter()

	r.Group(func(r chi.Router) {
		r.Use(jwtauth.Verifier(tokenAuth))
		r.Use(jwtauth.Authenticator)

		// ruleid: chi-route-authenticated
		r.Get("/admin", func(w http.ResponseWriter, r *http.Request) {
			_, claims, _ := jwtauth.FromContext(r.Context())
			w.Write([]byte(fmt.Sprintf("protected area. hi %v", claims["user_id"])))
		})
	})

	r.Group(func(r chi.Router) {
		// ruleid: chi-route-unauthenticated
		r.Get("/", func(w http.ResponseWriter, r *http.Request) {
			w.Write([]byte("welcome anonymous"))
		})
	})

	return r
}

func registerAPI(r *chi.Mux) {
	r.Route("/", func(r chi.Router) {
		r.Use(oauth.Authorize("mySecretKey", nil))

		// ruleid: chi-route-authenticated
		r.Get("/customers", GetCustomers)

		// ruleid: chi-route-authenticated
		r.Get("/customers/{id}/orders", GetOrders)
	})

	r.Route("/", func(r chi.Router) {
		// ruleid: chi-route-unauthenticated
		r.Get("/customers", GetCustomers)

		// ruleid: chi-route-unauthenticated
		r.Get("/customers/{id}/orders", GetOrders)
	})
}

func registerAPI(r *chi.Mux) {
	r.Route("/", func(r chi.Router) {
		r.Use(middleware.BasicAuth("realm", map[string]string{"user": "pass"}))

		// ruleid: chi-route-authenticated
		r.Get("/customers", GetCustomers)
	})

	r.Route("/", func(r chi.Router) {
		// ruleid: chi-route-unauthenticated
		r.Get("/customers", GetCustomers)
	})
}
