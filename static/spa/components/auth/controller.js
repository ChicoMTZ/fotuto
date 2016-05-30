fotuto.controller('AuthController', ['$scope', '$mdDialog', function ($scope, $mdDialog) {
	$scope.showLogin = function () {
		$mdDialog.show({
			controller: 'LoginController',
			templateUrl: '/static/spa/components/auth/login-form.html',
			parent: angular.element(document.body),
			clickOutsideToClose: true
		});
	}
}])
	.controller('LoginController', ['$scope', '$mdDialog', '$http', '$cookies', '$log',
		function ($scope, $mdDialog, $http, $cookies, $log) {
			$scope.cancel = function () {
				$mdDialog.hide();
			};
			$scope.login = function () {
				var user_data = {
					"username": $scope.user.username,
					"password": $scope.user.password
				};
				// Clear current token
				delete $http.defaults.headers.common['Authorization'];
				$cookies.remove('csrftoken');
				// Request for new token
				$http.post("/api/token/", user_data)
					.success(function (response) {
						$cookies.put('csrftoken', response.token);
						$http.defaults.headers.common['Authorization'] = 'Token ' + response.token;
					});
				$log.debug("login()...");
				$mdDialog.hide();
			};
		}]);
