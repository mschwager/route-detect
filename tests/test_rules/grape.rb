module Twitter
  class API < Grape::API
    version 'v1', using: :header, vendor: 'twitter'
    format :json
    prefix :api

    helpers do
      def current_user
        @current_user ||= User.authorize!(env)
      end

      def authenticate!
        error!('401 Unauthorized', 401) unless current_user
      end
    end

    resource :statuses do
      desc 'Return a public timeline.'
      # ruleid: grape-route-unauthenticated
      get :public_timeline do
        Status.limit(20)
      end

      desc 'Return a personal timeline.'
      # ruleid: grape-route-authenticated
      get :home_timeline do
        authenticate!
        current_user.statuses.limit(20)
      end

      desc 'Return a personal timeline.'
      # ruleid: grape-route-authenticated
      get :home_timeline do
        authenticate!
        authorize!
        current_user.statuses.limit(20)
      end

      desc 'Return a personal timeline.'
      # ruleid: grape-route-authorized
      get :home_timeline do
        authorize!
        current_user.statuses.limit(20)
      end

      desc 'Return a status.'
      params do
        requires :id, type: Integer, desc: 'Status ID.'
      end
      route_param :id do
        # ruleid: grape-route-unauthenticated
        get do
          Status.find(params[:id])
        end
      end

      desc 'Create a status.'
      params do
        requires :status, type: String, desc: 'Your status.'
      end
      # ruleid: grape-route-authenticated
      post do
        authenticate!
        Status.create!({
          user: current_user,
          text: params[:status]
        })
      end

      desc 'Update a status.'
      params do
        requires :id, type: String, desc: 'Status ID.'
        requires :status, type: String, desc: 'Your status.'
      end
      # ruleid: grape-route-authenticated
      put ':id' do
        authenticate!
        current_user.statuses.find(params[:id]).update({
          user: current_user,
          text: params[:status]
        })
      end

      desc 'Delete a status.'
      params do
        requires :id, type: String, desc: 'Status ID.'
      end
      # ruleid: grape-route-authenticated
      delete ':id' do
        authenticate!
        current_user.statuses.find(params[:id]).destroy
      end
    end
  end

  class API < Grape::API
    helpers do
      def current_user
        User.find(params[:user_id])
      end

      def authenticate!
        error!('401 Unauthorized', 401) unless current_user
      end
    end

    helpers StatusHelpers, HttpCodesHelpers

    before do
      authenticate!
    end

    # ruleid: grape-route-authenticated
    get 'info' do
      user_info(current_user)
    end
  end

  class API < Grape::API
    helpers do
      def current_user
        User.find(params[:user_id])
      end

      def authenticate!
        error!('401 Unauthorized', 401) unless current_user
      end
    end

    helpers StatusHelpers, HttpCodesHelpers

    before { authenticate! }

    # ruleid: grape-route-authenticated
    get 'info' do
      user_info(current_user)
    end
  end
end
