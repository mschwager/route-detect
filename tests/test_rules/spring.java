package test.routes;

import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.security.access.prepost.PreAuthorize;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.web.SecurityFilterChain;

import org.apache.shiro.authz.annotation.RequiresAuthentication;

@RestController
public class ExampleResource {

    // ruleid: spring-route-unauthenticated
    @RequestMapping(value = "/test", method = RequestMethod.GET)
    public Response myUnsecuredMethod(@PathParam("id") Long id) {
        return Response.ok().build();
    }

    // ruleid: spring-route-unauthenticated
    @DeleteMapping(value = "/test")
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

    // ruleid: spring-route-authorized
    @RequestMapping(value = "/test", method = RequestMethod.GET)
    @javax.annotation.security.RolesAllowed("role")
    public Response mySecuredMethod(@PathParam("id") Long id) {
        return Response.ok().build();
    }

    // ruleid: spring-route-authorized
    @RequestMapping(value = "/test", method = RequestMethod.GET)
    @jakarta.annotation.security.RolesAllowed("role")
    public Response mySecuredMethod(@PathParam("id") Long id) {
        return Response.ok().build();
    }

    // ruleid: spring-route-authenticated
    @RequestMapping(value = "/test", method = RequestMethod.GET)
    @RequiresAuthentication
    public Response mySecuredMethod(@PathParam("id") Long id) {
        return Response.ok().build();
    }

    // ruleid: spring-route-authorized
    @RequestMapping(value = "/test", method = RequestMethod.GET)
    @PreAuthorize("#oauth2.hasScope('server')")
    public Response mySecuredMethod(@PathParam("id") Long id) {
        return Response.ok().build();
    }
}

@PreAuthorize("hasRole('ROLE_ADMIN')")
public class ExampleResource {

    // ruleid: spring-route-authorized
    @RequestMapping(value = "/test", method = RequestMethod.GET)
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

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        // ruleid: spring-route-global-authenticated
        http.authorizeHttpRequests()
            .requestMatchers("/**")
            .hasRole("USER")
            .and()
            .formLogin();

        return http.build();
    }
}

@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        // ruleid: spring-route-global-authenticated
        http.authorizeRequests()
            .anyRequest()
            .authenticated()
            .and()
            .formLogin()
            .and()
            .httpBasic();
    }
}
