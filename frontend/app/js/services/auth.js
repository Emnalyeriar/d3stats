'use strict';

function Auth($cookies, $http) {

  const Auth = {};

  Auth.register = function(email, password, username, confirm_password) {
    return $http.post('http://localhost:8080/api/v1/accounts/', {
      username: username,
      password: password,
      email: email,
      confirm_password: confirm_password
    }).then(registerSuccessFn, loginErrorFn);
  };
  Auth.registerSuccessFn = function(data, status, headers, config) {
    Auth.login(username, password);
  };
  Auth.registerErrorFn = function(data, status, headers, config) {
    console.log('error');
  };
  Auth.login = function(username, password) {
    return $http.post('http://localhost:8080/api/v1/auth/login/', {
      username: username,
      password: password
    }).then(Auth.loginSuccessFn, Auth.loginErrorFn);
  };
  Auth.loginSuccessFn = function(data, status, headers, config) {
    console.log(arguments);
    Auth.setAuthenticatedAccount(data.data);
    // window.location = '/';
  };
  Auth.loginErrorFn = function(data, status, headers, config) {
    console.log('error!');
  };
  Auth.getAuthenticatedAccount = function() {
    if (!$cookies.getObject('authenticatedAccount')) {
      return;
    };
    return $cookies.getObject('authenticatedAccount');
  };
  Auth.isAuthenticated = function() {
    return !!$cookies.getObject('authenticatedAccount');
  };
  Auth.setAuthenticatedAccount = function(account) {
    console.log(account);
    // $cookies.authenticatedAccount = JSON.stringify(account);
    $cookies.putObject('authenticatedAccount', account);
  };
  Auth.unauthenticate = function() {
    $cookies.remove('authenticatedAccount');
  };
  Auth.logout = function() {
    return $http.post('http://localhost:8080/api/v1/auth/logout/').then(Auth.logoutSuccessFn, Auth.logoutErrorFn);
  };
  Auth.logoutSuccessFn = function() {
    Auth.unauthenticate();
    // window.location = '/';
  };
  Auth.logoutErrorFn = function() {
    console.log('error');
  };
  return Auth;
}

export default {
  name: 'Auth',
  fn: Auth
};
