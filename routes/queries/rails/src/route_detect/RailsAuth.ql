/**
 * @name Rails route-detect auth query
 * @id route-detect/rails/auth
 * @description TODO
 * @kind problem
 * @tags rd_fill=green
 * @problem.severity error
 * @precision medium
 */

import codeql.ruby.frameworks.ActionController
import codeql.ruby.frameworks.ActionDispatch

import route_detect.Auth

from ActionControllerActionMethod method, ActionDispatch::Routing::Route r
where
    (
        authControllerCall(_, method.getControllerClass(), _) or
        authActionCall(method)
    ) and
    method.getARoute() = r
select r, "Found authed Rails route," +
          " method=" + r.getHttpMethod() +
          " path=" + r.getPath() +
          " controller=" + r.getController() +
          " action=" + r.getAction()
