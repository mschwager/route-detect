import codeql.ruby.ApiGraphs
import codeql.ruby.AST
import codeql.ruby.DataFlow
import codeql.ruby.frameworks.ActionController
import codeql.ruby.frameworks.ActionDispatch

API::Node actionControllerInstance() {
  result = any(ActionControllerClass cls).getSelf().track()
}

class AuthCall extends DataFlow::CallNode {
    AuthCall() {
        (
            this = actionControllerInstance().getAMethodCall("before_action") and
            (
                // require_authentication is a Rails 8 method:
                // https://github.com/rails/rails/blob/v8.0.0/railties/lib/rails/generators/rails/authentication/templates/app/controllers/concerns/authentication.rb.tt
                this.getArgument(0).getConstantValue().isStringlikeValue("require_authentication") or
                // authenticate_user! is a Devise method:
                // https://github.com/heartcombo/devise#controller-filters-and-helpers
                this.getArgument(0).getConstantValue().isStringlikeValue("authenticate_user!") or
                // doorkeeper_authorize! is a Doorkeeper method:
                // https://doorkeeper.gitbook.io/guides/ruby-on-rails/protecting-your-resources
                this.getArgument(0).getConstantValue().isStringlikeValue("doorkeeper_authorize!")
            )
        ) or
        (
            // authorize_resource and load_and_authorize_resource are CanCanCan methods:
            // https://github.com/CanCanCommunity/cancancan/blob/develop/docs/controller_helpers.md#authorize_resource-load_resource-load_and_authorize_resource
            this = actionControllerInstance().getAMethodCall("authorize_resource") or
            this = actionControllerInstance().getAMethodCall("load_and_authorize_resource")
        )
    }
}

predicate authControllerCall(
  ActionControllerClass parent, ActionControllerClass child, AuthCall call
) {
  parent.getSelf().flowsTo(call.getReceiver()) and child = parent.getADescendent()
}

predicate authActionCall(ActionControllerActionMethod method) {
    exists(MethodCall mc |
        mc.getMethodName() = [
            // authorize is a Pundit method:
            // https://github.com/varvet/pundit#policies
            "authorize",
            // authorize! is a CanCanCan method:
            // https://github.com/CanCanCommunity/cancancan/blob/develop/docs/controller_helpers.md#authorize
            "authorize!",
        ] and
        method.getAChild() = mc
    )
}
