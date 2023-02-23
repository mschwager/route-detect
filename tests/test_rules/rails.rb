Rails.application.routes.draw do
  # ruleid: rails-route
  resources :brands, only: [:index, :show] do
    # ruleid: rails-route
    resources :products, only: [:index, :show]
  end

  # ruleid: rails-route
  resource :basket, only: [:show, :update, :destroy]

  # ruleid: rails-route
  resources :photos

  # ruleid: rails-route
  resources :photos, :books, :videos

  # ruleid: rails-route
  resources :photos do
    collection do
      # ruleid: rails-route
      get 'search'
    end
  end

  # ruleid: rails-route
  match 'photos', to: 'photos#show', via: [:get, :post]

  resolve("Basket") { route_for(:basket) }
end
