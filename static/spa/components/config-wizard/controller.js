fotuto.controller('DeviceController', ['$scope', '$http', function ($scope, $http) {

	/**
	 * Devices
	 *
	 * Example device: {'name':'Door Sensor', 'slug': 'door-sensor', 'address': '0001'}
	 *
	 * @type {Array}
	 */
	$scope.device = {};
	$scope.devices = [];

	$http.get('/api/devices/').success(function (data) {
		$scope.devices = data.results;
	});

	$scope.add = function () {
		$http.post('/api/devices/', $scope.device)
			.success(function (data) {
				$scope.result = data;
				$scope.devices.unshift(data);
				$scope.device = {};
			})
			.error(function (data) {
				$scope.error = data;
			});
	}
}]);

fotuto.controller('VarController', ['$scope', '$http', function ($scope, $http) {

	/**
	 * Variables
	 *
	 * Example variable: {'name':'Door Status', 'device': 1, 'var_type': 'digital'}
	 *
	 * @type {Array}
	 */
	$scope.var = {};
	$scope.vars = [];
	$scope.devices = []; // TODO: Optimize: devices should be shared with DeviceController

	$http.get('/api/vars/').success(function (data) {
		$scope.vars = data.results;
	});

	// TODO: Optimize: devices are shared this request don't needed
	$http.get('/api/devices/').success(function (data) {
		$scope.devices = data.results;
	});

	$scope.add = function () {
		$http.post('/api/vars/', $scope.var)
			.success(function (data) {
				$scope.result = data;
				$scope.vars.unshift($scope.var);
				$scope.var = {};
			})
			.error(function (data) {
				$scope.error = data;
			});
	}
}]);

fotuto.controller('SceneController', ['$scope', '$http', function ($scope, $http) {

	/**
	 * Scenes
	 *
	 * Example : {'title':'Alarm System', 'slug': 'alarm-system', 'description': 'Some descripion'}
	 *
	 * @type {Array}
	 */
	$scope.scene = {};
	$scope.scenes = [];

	$http.get('/api/windows/').success(function (data) {
		$scope.scenes = data.results;
	});

	$scope.add = function () {
		$http.post('/api/windows/', $scope.scene)
			.success(function (data) {
				$scope.result = data;
				$scope.scenes.unshift($scope.scene);
				$scope.scene = {};
			})
			.error(function (data) {
				$scope.error = data;
			});
	}
}]);

fotuto.controller('MimicController', ['$scope', '$http', function ($scope, $http) {

	/**
	 * Mimics
	 *
	 * Example mimic: {"name": "Door Sensor", "window": 1, "vars": [1,2], 'x': 100, "y": 100}
	 *
	 * @type {Array}
	 */
	$scope.mimic = {};
	$scope.mimics = [];
	$scope.vars = []; // TODO: Optimize: vars should be shared with VarController
	$scope.scenes = []; // TODO: Optimize: scenes should be shared with SceneController

	$http.get('/api/mimics/').success(function (data) {
		$scope.mimics = data.results;
	});

	// TODO: Optimize: vars are shared this request don't needed
	$http.get('/api/vars/').success(function (data) {
		$scope.vars = data.results;
	});

	// TODO: Optimize: scenes are shared this request don't needed
	$http.get('/api/windows/').success(function (data) {
		$scope.scenes = data.results;
	});

	// TODO: Implement update mimic

	$scope.save = function () {
		$http.post('/api/mimics/', $scope.mimic)
			.success(function (data) {
				$scope.result = data;
				$scope.mimics.unshift($scope.mimic);
				$scope.mimic = {};
			})
			.error(function (data) {
				$scope.error = data;
			});
	}
}]);
