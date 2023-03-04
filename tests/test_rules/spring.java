package test.routes;

import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.security.access.prepost.PreAuthorize;

import javax.annotation.security.RolesAllowed;

@RestController
public class ExampleResource {

    // ruleid: spring-route-unauthenticated
    @RequestMapping(value = "/test", method = RequestMethod.GET)
    public Response myUnsecuredMethod(@PathParam("id") Long id) {
        return Response.ok().build();
    }

    // ruleid: spring-route-authenticated
    @RequestMapping(value = "/test", method = RequestMethod.GET)
    @Secured
    public Response mySecuredMethod(@PathParam("id") Long id) {
        return Response.ok().build();
    }

    // ruleid: spring-route-authenticated
    @Secured
    @RequestMapping(value = "/test", method = RequestMethod.GET)
    public Response mySecuredMethod(@PathParam("id") Long id) {
        return Response.ok().build();
    }

    // ruleid: spring-route-authenticated
    @RequestMapping(value = "/test", method = RequestMethod.GET)
    @RolesAllowed("role")
    public Response mySecuredMethod(@PathParam("id") Long id) {
        return Response.ok().build();
    }

    // ruleid: spring-route-authenticated
    @RequestMapping(value = "/test", method = RequestMethod.GET)
    @PreAuthorize("#oauth2.hasScope('server')")
    public Response mySecuredMethod(@PathParam("id") Long id) {
        return Response.ok().build();
    }
}

public interface ExampleInterface {

    // todoruleid: spring-route-authenticated
    @RequestMapping(value = "/test", method = RequestMethod.GET)
    @Secured
    void myInterface(@PathParam("id") Long id);
}
