class PostsController < ApplicationController
  def index
  end

  def show
    @post = Post.find(params[:id])
    authorize @post, :show?
    @post.show!
  end
end
