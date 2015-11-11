'use strict';

function HomeCtrl($scope, Auth) {

  $scope.login = function () {
    Auth.login($scope.username, $scope.password);
  };

  $scope.logout = function () {
    Auth.logout();
  };

}

export default {
  name: 'HomeCtrl',
  fn: HomeCtrl
};
