/**
 * @name Rails route-detect query
 * @id route-detect/rails
 * @description TODO
 * @kind problem
 * @tags security
 * @problem.severity error
 * @precision medium
 */

import codeql.ruby.frameworks.ActionDispatch

from ActionDispatch::Routing::Route r
select r, "Found Rails route"
