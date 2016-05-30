describe('Configuration Wizard Step 1: Devices', function () {
	var $scope = {};
	var $httpBackend;

	beforeEach(module('fotuto'));

	beforeEach(angular.mock.module('templates'));

	beforeEach(inject(function ($controller, $rootScope, _$httpBackend_) {

		// Mock http
		$httpBackend = _$httpBackend_;
		$httpBackend.expectGET("/api/devices/").respond({
			results: [
				{'name': 'Alarm Controller', 'address': '0001'},
				{'name': 'Door Sensor', 'address': '0002'}
			]
		});

		$scope = $rootScope.$new();
		$controller('DeviceController', {$scope: $scope});
	}));

	afterEach(function () {
		$httpBackend.verifyNoOutstandingExpectation();
		$httpBackend.verifyNoOutstandingRequest();
	});

	it('Controller should add Devices', function () {
		$httpBackend.expectPOST('/api/devices/').respond(200, {
			'name': 'Door 2 Sensor',
			'address': '0003'
		});
		$scope.add({
			'name': 'Door 2 Sensor',
			'address': '0003'
		});
		$httpBackend.flush();

		expect($scope.devices[0].name).toBe('Door 2 Sensor');
	});

	it('should create "devices" model with 2 devices fetched from api', function () {
		expect($scope.devices).toEqual([]);
		$httpBackend.flush();
		expect($scope.devices).toEqual([
			{'name': 'Alarm Controller', 'address': '0001'},
			{'name': 'Door Sensor', 'address': '0002'}
		]);
	});
});