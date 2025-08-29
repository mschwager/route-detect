/**
 * @name Sinatra route-detect query
 * @id route-detect/sinatra
 * @description TODO
 * @kind problem
 * @tags security
 * @problem.severity error
 * @precision medium
 */

import codeql.ruby.frameworks.Sinatra

from Sinatra::Route r
select r, "Found Sinatra route"
