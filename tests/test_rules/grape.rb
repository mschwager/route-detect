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

    # todoruleid: grape-route-authenticated
    resource :statuses do
      desc 'Return a public timeline.'
      # todoruleid: grape-route-authenticated
      get :public_timeline do
        Status.limit(20)
      end

      desc 'Return a personal timeline.'
      # ruleid: grape-route-authenticated
      get :home_timeline do
        authenticate!
        current_user.statuses.limit(20)
      end

      desc 'Return a status.'
      params do
        requires :id, type: Integer, desc: 'Status ID.'
      end
      route_param :id do
        # todoruleid: grape-route-authenticated
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
end
