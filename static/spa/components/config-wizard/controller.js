fotuto.controller('DeviceController', ['$scope', function ($scope) {

	/**
	 * Devices
	 *
	 * Example device: {'name':'Door Sensor', 'slug': 'door-sensor', 'address': '0001'}
	 *
	 * @type {Array}
	 */
	$scope.devices = [];
	$scope.device = {};

	$scope.add = function (device) {
		$scope.devices.unshift(device);
		$scope.device = {};
	}
}]);