/**
 * @name Rails route-detect unauth query
 * @id route-detect/rails/unauth
 * @description TODO
 * @kind problem
 * @tags rd_fill=red
 * @problem.severity error
 * @precision medium
 */

import codeql.ruby.frameworks.ActionController
import codeql.ruby.frameworks.ActionDispatch

import route_detect.Auth

from ActionControllerActionMethod method, ActionDispatch::Routing::Route r
where
    not authControllerCall(_, method.getControllerClass(), _) and
    not authActionCall(method) and
    method.getARoute() = r
select r, "Found unauthed Rails route," +
          " method=" + r.getHttpMethod() +
          " path=" + r.getPath() +
          " controller=" + r.getController() +
          " action=" + r.getAction()
