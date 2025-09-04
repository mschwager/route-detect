Rails.application.routes.draw do
  resources :widgets, only: [:show, :index]
  resources :users, only: [:show, :index]
  resources :posts, only: [:show, :index]
end
