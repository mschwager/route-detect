package test.routes;

import io.swagger.annotations.Api;
import io.swagger.annotations.Authorization;

import javax.annotation.security.RolesAllowed;
import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.DELETE;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

@Path("/example")
public class ExampleResource {

    // ruleid: jaxrs-route-unauthenticated
    @GET
    @Path("{id}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response myUnsecuredMethod(@PathParam("id") Long id) {
        return Response.ok().build();
    }

    // ruleid: jaxrs-route-authenticated
    @DELETE
    @Secured
    @Path("{id}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response mySecuredMethod(@PathParam("id") Long id) {
        return Response.ok().build();
    }

    // ruleid: jaxrs-route-authenticated
    @DELETE
    @RolesAllowed("role")
    @Path("{id}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response mySecuredMethod(@PathParam("id") Long id) {
        return Response.ok().build();
    }
}

@Path("/v1/path")
@Api(value = "path", authorizations = @Authorization(value = "X-Api-Key"))
public class ExampleResource extends AbstractExampleResource {

    // ruleid: jaxrs-route-authenticated
    @DELETE
    @Path("{id}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response mySecuredMethod(@PathParam("id") Long id) {
        return Response.ok().build();
    }
}

@Path("/v1/path")
@Secured
public class ExampleResource extends AbstractExampleResource {

    // ruleid: jaxrs-route-authenticated
    @DELETE
    @Path("{id}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response mySecuredMethod(@PathParam("id") Long id) {
        return Response.ok().build();
    }
}
