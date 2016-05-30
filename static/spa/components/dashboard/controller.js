fotuto.controller('DashboardController', ['$scope', '$http', '$interval', '$filter', '$log',
	function ($scope, $http, $interval, $filter, $log) {

		$scope.scenes = [];
		$scope.last_update = new Date();
		$scope.updating = false;

		$http.get('/api/windows/').success(function (data) {
			$scope.scenes = data.results;
			try {
				$scope.showScene($scope.scenes[0].id)
			} catch (err) {
				$log.warn("There is no scene to display")
			}
		});

		$scope.showScene = function (scene_id) {
			$scope.scene = $filter('filter')($scope.scenes, {id: scene_id}, true)[0];
			$http.get('/api/mimics/?window=' + scene_id).success(function (data) {
				$scope.scene.mimics = data.results;
				$scope.init_updates();
			});
		};

		// Update values
		$scope.init_updates = function () {
			$interval.cancel($scope.interval_promise);
			$scope.interval_promise = $interval(
				function () {
					// TODO: Display/hide the "updating..." indicator
					/* TODO: Optimize: it should be better if api provide the endpoint `/api/windows/<window.pk>/values/` with in
					 results field the list of variable values i.e. [{"slug": "some-var", "value": 0.5}]
					 */
					$scope.updating = true;
					$http.get('/api/vars/?mimic__window=' + $scope.scene.id).then(function (response) {
						// TODO: Use this date from the server to not depend of the client date
						// Update variables's values
						// Finds each mimic in current scene
						$scope.scene.mimics.forEach(function (mimic, index) {
							// Define all vars as parameters for var value transform function and all vars
							// for this mimic
							// TODO: Take aware that a mimic can have the same var twice or more with different rules
							var parameters_names = mimic.vars.map(function(v) {return v.slug});
							var parameters_values = response.data.results.map(
								function(v) {
									return (parameters_names.indexOf(v.slug) == -1)?0:v.value;
								}
							);
							parameters_names.unshift('min', 'max');

							mimic.vars.forEach(
								function (variable, index) {
									variable.value = $filter('getItem')(response.data.results, variable.slug, true).value;
									// Search for rule
									var rule = $filter('getItem')(mimic.rules, {var: variable.id}, true);
									if (rule) {
										// Apply rule
										// TODO: Maybe this should be cached
										// TODO: sanitize var slugs?
										// Create operation function to transform var's value
										var operation = new Function(parameters_names, rule.operation);
										var rule_parameters_values = parameters_values.slice();
										rule_parameters_values.unshift(rule.min, rule.max);
										variable.value = operation.apply(this, rule_parameters_values);
										//d3.select('.' + variable.slug).attr(rule.attr, value);
									}
								}
							);
						});
						$scope.last_update = new Date();
						$scope.updating = false;
					}, function (err) {
						throw err;
					});
				}, 3000
			); // TODO: Move this interval to a settings page
		}
	}
]);
